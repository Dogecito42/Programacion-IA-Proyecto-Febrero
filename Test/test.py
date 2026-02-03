#Hacer un Script en Python para que mande a InfluxDB simular los daots de lectura:

# Debe mandar los datos de cada una de las aulas asignadas (igual que con los sensores).

#Los rangos que debe simular son :

#1. Rango entre 350 - 500 aleatoriamente

#2. Calcular un 5% de probabilidad de que envie un dato entre 700 - 800. Esto solo puede ocurrir en los timestamp de de 8:00 a 15:00, y 16:15 a 22:15

import requests
import time
import random

# CONFIGURACIÓN INFLUXDB

INFLUX_URL = "https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/write" # URL de nuestra Instancia
INFLUX_TOKEN = "kgyUOT23smNqrVSDObXpopNZKjqZ_xFtR0FdLHYIhq1He32Pt0MNBDQj3KquyMgYNHdj1jgSuKbPW00ulYGaBA=="
INFLUX_ORG = "MaderoData"
INFLUX_BUCKET = "data-test-1"
CLASSROOM = 211

# SIMULACIÓN DE DATOS

# Por cuenta propia para dar un bloque más realista
  # Verifica si la hora actual está en horario de pico:
  # - 8:00 a 15:00
  # - 16:15 a 22:15
  # La verificación se hace contando los minutos desde las 00:00 (min 0)
def esta_en_horario_pico():
    ahora = time.localtime()
    hora = ahora.tm_hour
    minuto = ahora.tm_min

    # Convertir a minutos desde 00:00
    minutos_del_dia = hora * 60 + minuto

    # Rango 1: 8:00 a 15:00
    INICIO_MANANA = 8 * 60
    FIN_MANANA = 15 * 60

    # Rango 2: 16:15 a 22:00
    INICIO_TARDE = 16 * 60 + 15
    FIN_TARDE = 22 * 60

    en_horario_manana = INICIO_MANANA <= minutos_del_dia < FIN_MANANA
    en_horario_tarde = INICIO_TARDE <= minutos_del_dia < FIN_TARDE

    return en_horario_manana or en_horario_tarde

# Genera un valor simulado:
# - 95% de probabilidad: valor "normal"
# - 5% de probabilidad: valor "alto" (solo en horario clase)
def generar_valor_simulado():
    if esta_en_horario_pico() and random.random() < 0.02:
        # 5% de probabilidad de valor alto en horario clase
        return random.randint(700, 800)
    else:
        # Valor normal
        return random.randint(350, 500)

# ENVIAR A INFLUXDB

def enviar_influx(valor):
    print("Enviando valor a InfluxDB:", valor)
    headers = {
        "Authorization": "Token " + INFLUX_TOKEN,
        "Content-Type": "text/plain; charset=utf-8"
    }

    data = "noiselevel,classroom={} valor={}".format(CLASSROOM, valor)

    url = "{}?org={}&bucket={}&precision=s".format(
        INFLUX_URL, INFLUX_ORG, INFLUX_BUCKET
    )

    try:
        r = requests.post(url, headers=headers, data=data)
        if r.status_code == 204:
            print("Dato enviado:", valor)
        else:
            print("Error HTTP {}: {}".format(r.status_code, r.text))
    except Exception as e:
        print("Error enviando a InfluxDB:", e)

# main
while True:
    valor_simulado = generar_valor_simulado()
    enviar_influx(valor_simulado)
    time.sleep(5)