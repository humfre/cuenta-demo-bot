# -*- coding: utf-8 -*-

from iqoptionapi.api import IQOptionAPI
import time
import logging
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configurar el registro de eventos
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Datos de inicio de sesión (obtenidos desde variables de entorno)
email = os.getenv("IQ_OPTION_EMAIL")
print(email)
password = os.getenv("IQ_OPTION_PASSWORD")
print(password)

# Conectar a IQ Option (modo demo)
api = IQOptionAPI(email, password)
print(api)
try:
    api.connect()
    print("Connection successful!")
except Exception as e:
    logging.error(f"Connection failed: {e}")  

# Verificar la conexión
if api.check_connect():
    logging.info("Conexión exitosa a IQ Option")
else:
    logging.error("Error al conectar a IQ Option")
    exit()

# Parámetros de trading
activo = "EURUSD"
tiempo_expirar = 1  # 1 minuto
cantidad_invertir = 1  # $1 por operación
stop_loss = 0.02  # 2% de pérdida máxima (opcional)
take_profit = 0.04  # 4% de ganancia objetivo (opcional)

# Función para calcular indicadores (simplificado para demostración)
def calcular_indicadores():
    try:
        # Obtener datos históricos o en tiempo real
        # Aquí se simulan valores para los indicadores (ajustar según tus datos)
        media_corta = 50  # Ejemplo de media corta (ajustar según tu estrategia)
        media_larga = 200  # Ejemplo de media larga (ajustar según tu estrategia)
        rsi = 40  # Ejemplo de RSI (ajustar según tu estrategia)

        return media_corta, media_larga, rsi

    except Exception as e:
        logging.error(f"Error al calcular indicadores: {e}")
        return None, None, None

# Función para ejecutar una operación
def ejecutar_operacion(direccion):
    try:
        result, id = api.buy(cantidad_invertir, activo, direccion, tiempo_expirar)
        if result:
            logging.info(f"Operación {direccion} abierta para {activo} (ID: {id})")
            return id
        else:
            logging.error(f"Error al abrir la operación {direccion} para {activo}: {api.last_candles_error}")
    except Exception as e:
        logging.error(f"Error inesperado al ejecutar operación: {e}")

# Ejemplo de ejecución basado en condiciones
try:
    while True:  # Bucle continuo para ejecución continua
        # Calcular indicadores
        media_corta, media_larga, rsi = calcular_indicadores()

        # Verificar si se pudieron calcular los indicadores
        if media_corta is None or media_larga is None or rsi is None:
            logging.error("No se pudieron calcular los indicadores. Deteniendo la ejecución.")
            break

        # Definir condiciones de trading
        if media_corta > media_larga and rsi < 30:
            condition_to_buy = True
            condition_to_sell = False
        elif media_corta < media_larga and rsi > 70:
            condition_to_buy = False
            condition_to_sell = True
        else:
            condition_to_buy = False
            condition_to_sell = False

        # Ejecutar operaciones basadas en las condiciones
        if condition_to_buy:
            ejecutar_operacion("call")
        elif condition_to_sell:
            ejecutar_operacion("put")
        else:
            logging.info("Sin señales de trading detectadas. Esperando próxima iteración.")

        time.sleep(5)  # Esperar 5 segundos antes de la próxima iteración

except KeyboardInterrupt:
    logging.info("Detención del programa mediante teclado.")
except Exception as e:
    logging.error(f"Error en la ejecución: {e}")

# Cerrar la conexión al finalizar
api.close_connect()
