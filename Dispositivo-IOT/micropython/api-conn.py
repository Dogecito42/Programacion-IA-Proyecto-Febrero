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
# CONFIGURACIÓN API REST
# ======================
API_URL = "http://127.0.0.1:80/send-to-db"

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
# ENVIAR A API REST
# ======================
def enviar_api(valor):
    headers = {
        "Content-Type": "application/json"
    }

    try:
        r = urequests.post(API_URL, headers=headers, data=str(valor))
        r.close()
        print("Dato enviado:", valor)
    except Exception as e:
        print("Error enviando a API:", e)

# ======================
# PROGRAMA PRINCIPAL
# ======================
conectar_wifi()

while True:
    valor_adc = adc.read()
    enviar_api(valor_adc)
    time.sleep(5)   # cada 5 segundos