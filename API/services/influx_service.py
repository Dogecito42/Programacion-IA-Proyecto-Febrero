import requests

# ======================
# CONFIGURACIÓN INFLUXDB
# ======================
INFLUX_URL = "https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/write"
INFLUX_TOKEN = "URgMUmpnvIURZXChEvJNpquFuN9hYYsL7A5-SrKwUNrccBeOraPpZviYP7ar8lAAUck3ijcxN4-tCFQtUirHpA=="
INFLUX_ORG = "3bc9f1a9bad6ea86"
INFLUX_BUCKET = "noiseLevel"
CLASSROOM = 209


def enviar_influx(valor: int) -> bool:
    """Envía un valor a InfluxDB."""
    headers = {
        "Authorization": f"Token {INFLUX_TOKEN}",
        "Content-Type": "text/plain; charset=utf-8"
    }

    data = f"noiselevel,classroom={CLASSROOM} valor={valor}"
    url = f"{INFLUX_URL}?org={INFLUX_ORG}&bucket={INFLUX_BUCKET}&precision=s"

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        print(f"Dato enviado a InfluxDB: {valor}")
        return True
    except Exception as e:
        print(f"Error enviando a InfluxDB: {e}")
        return False
