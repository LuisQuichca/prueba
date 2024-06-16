from flask import Flask, render_template, request, jsonify

## Database
import datetime
import pytz
from google.oauth2 import service_account
import pandas as pd
import backend
from google.cloud import bigquery

app = Flask(__name__)
#tqa = pipeline(task="table-question-answering",model="google/tapas-large-finetuned-wtq") #1 seg

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/chatbot")
def chatbot():
    return render_template('chatbot.html')

@app.route("/notificaciones")
def notificaciones():
    not1, not2, not3 = notificaciones_funcion()

    return render_template('notificaciones.html', not1=not1, not2=not2,not3=not3)

@app.route('/pregunta', methods=['POST'])
def pregunta():
    user_input = request.form['user']
    respuesta = backend.consulta(user_input)
    return jsonify({'respuesta': respuesta})
    #return render_template('index_respuesta.html', pregunta=user_input, respuesta=respuesta)

def notificaciones_funcion():
    # define tables and credentials  
    credentials_path = 'assitania-62cd2f864f41.json'
    project_id = "assitania"
    dataset_id = "pe_proy_sales"
    table_Sales_Predictions = "SalesPredictions"
    table_Sales = "Sales"
    # get the actual time 
    # Obtener la hora actual en Lima
    lima_tz = pytz.timezone('America/Lima')
    lima_time = datetime.datetime.now(lima_tz)

    # Obtener el número del mes actual y el siguiente mes
    current_month = lima_time.month
    next_month = (current_month % 12) + 1

    # Obtener la fecha actual y la fecha hace un año
    fecha_actual = datetime.datetime.now()
    fecha_hace_un_anio = fecha_actual - datetime.timedelta(days=365)
    
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = bigquery.Client(credentials=credentials)

    query_predictions = f"SELECT * FROM `{project_id}.{dataset_id}.{table_Sales_Predictions}`"
    df_predictions = client.query(query_predictions).to_dataframe()

    query_sales = f"SELECT * FROM `{project_id}.{dataset_id}.{table_Sales}`"
    df_sales = client.query(query_sales).to_dataframe()

    # Notifcaciones tabla Predictions
    df_predictions['month_date'] = pd.to_datetime(df_predictions['date']).dt.month
    df_filter = df_predictions[df_predictions.month_date == next_month]
    indice_fila_min = df_filter['prediction_rf'].idxmin()
    df_max = df_filter.nlargest(2, 'prediction_rf').reset_index(drop=True)
    fila_con_min = df_predictions.loc[indice_fila_min]

    # Notifcaciones tabla Sales
    df_sales['FECHA'] = pd.to_datetime(df_sales['FECHA'])
    Total_ventas = df_sales[df_sales.FECHA <= fecha_hace_un_anio]['TOTAL_LINEA'].sum()

    a = f"El código de producto con menor predicción de demanda para el siguiente mes es {fila_con_min['CODIGO_ARTICULO']}, con un monto de {fila_con_min['prediction_rf']} unidades"
    b = f"Los dos producto con mayor predicción de demanda para el siguiente mes son {df_max.iloc[0]['CODIGO_ARTICULO']} y {df_max.iloc[1]['CODIGO_ARTICULO']} , con un monto de {df_max.iloc[0]['prediction_rf']} y {df_max.iloc[1]['prediction_rf']} unidades"
    c = f"Para la fecha de {fecha_hace_un_anio.strftime('%Y/%m/%d')}, se tiene un total en ventas de S/. {round(Total_ventas,2)}"
    return a,b,c

if __name__ == '__main__':
    app.run(port=80)