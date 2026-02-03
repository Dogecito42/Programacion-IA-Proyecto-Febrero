from machine import Pin, ADC
import network
import urequests
import time

# ======================
# CONFIGURACIÓN WIFI
# ======================
WIFI_SSID = "Aula211_2G"
WIFI_PASS = "internet211"

# ======================
# CONFIGURACIÓN INFLUXDB
# ======================
INFLUX_URL = "https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/write" # URL de nuestra Instancia
INFLUX_TOKEN = "URgMUmpnvIURZXChEvJNpquFuN9hYYsL7A5-SrKwUNrccBeOraPpZviYP7ar8lAAUck3ijcxN4-tCFQtUirHpA=="
INFLUX_ORG = "3bc9f1a9bad6ea86"
INFLUX_BUCKET = "noiseLevel"
CLASSROOM = 209 # Aula

# ======================
# SENSOR ANALÓGICO
# ======================
adc = ADC(Pin(33))
adc.atten(ADC.ATTN_11DB)      # Rango completo ~0-3.3V
adc.width(ADC.WIDTH_12BIT)    # 0 - 4095

# ======================
# CONEXIÓN WIFI
# ======================
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Conectando a WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(0.5)

    print("WiFi conectado:", wlan.ifconfig())

# ======================
# ENVIAR A INFLUXDB
# ======================
def enviar_influx(valor):
    headers = {
        "Authorization": "Token " + INFLUX_TOKEN,
        "Content-Type": "text/plain; charset=utf-8"
    }

    data = "noiselevel,classroom={} valor={}".format(CLASSROOM, valor)

    url = "{}?org={}&bucket={}&precision=s".format(
        INFLUX_URL, INFLUX_ORG, INFLUX_BUCKET
    )

    try:
        r = urequests.post(url, headers=headers, data=data)
        r.close()
        print("Dato enviado:", valor)
    except Exception as e:
        print("Error enviando a InfluxDB:", e)

# ======================
# PROGRAMA PRINCIPAL
# ======================
conectar_wifi()

while True:
    valor_adc = adc.read()
    enviar_influx(valor_adc)
    time.sleep(5)   # cada 5 segundos