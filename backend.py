
from langchain.sql_database import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///bdgrupohidraulica.db")

# 2. Importar las APIs
import api_key
import os
os.environ["OPENAI_API_KEY"] = api_key.OPENAI_API_KEY

# 3. Crear el LLM
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(temperature=0,model_name='gpt-4')
#gpt-3.5-turbo

# 4. Crear la cadena
#from langchain import SQLDatabaseChain
from langchain_experimental.sql import SQLDatabaseChain
cadena = SQLDatabaseChain(llm = llm, database = db, verbose=False)


# 5. Formato personalizado de respuesta
formato = """
Eres un asistente virtual conversacional y recuerda que, Dada una pregunta del usuario:
1. Ten presente que eres un asistente virtual que tiene memoria y que busca conversar, Recuerda que a cada pregunta:
2. crea una consulta de sqlite3, si con la pregunta no puedes generar una consulta SQL, responde pidiendo consultas relacionadas a la base de datos y ya no hagas caso a las siguientes instrucciones
3. revisa los resultados
4. devuelve el dato en lineas de bajo para que se entienda
5. Recuerda que eres capaz de dar predicciones de ventas futuras de acuerdo al historial de ventas de la base de datos
6. A cada pregunta de predición crea un modelo predictivo e indica esa predicción
7. si tienes que hacer alguna aclaración o devolver cualquier texto que sea siempre en español
#{question}
"""

# 1. Ten presente que eres un asistente virtual que tiene memoria y que busca conversar, Recuerda que a cada pregunta:
# 2. A cada pregunta donde indique la palabra predición suma las ventas del mes en que te indiquen de acuerdo al historial de ventas del 2021 y 2022 , y como resultado muestra el promedio
# 4. crea una consulta de sqlite3
# 5. revisa los resultados
# 6. devuelve el dato en lineas de bajo para que se entienda
# 7. Recuerda que eres capaz de dar predicciones de ventas futuras de acuerdo al historial de ventas de la base de datos
# 8. si tienes que hacer alguna aclaración o devolver cualquier texto que sea siempre en español


# 1. crea una consulta de sqlite3
# 2. revisa los resultados
# 3. devuelve el dato
# 4. recuerda que tambien puedes dar estrategias o recomendaciones de venta
# 6. recuerda que eres capaz de dar predicciones de ventas futuras de acuerdo al historial de ventas de la base de datos
# 5. si tienes que hacer alguna aclaración o devolver cualquier texto que sea siempre en español

# 1. crea una consulta de sqlite3
# 2. revisa los resultados
# 3. devuelve el dato
# 4. recuerda que tambien puedes dar estrategias o recomendaciones de venta
# 6. recuerda que eres capaz de dar predicciones de ventas futuras de acuerdo al historial de ventas de la base de datos
# 5. si tienes que hacer alguna aclaración o devolver cualquier texto que sea siempre en español

# 6. Función para hacer la consulta

def consulta(input_usuario):
    consulta = formato.format(question = input_usuario)
    resultado = cadena.run(consulta)
    return(resultado)