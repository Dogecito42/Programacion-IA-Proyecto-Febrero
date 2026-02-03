from flask import Blueprint, request, jsonify
from services.influx_service import enviar_influx

db_bp = Blueprint('db', __name__)


@db_bp.route('/send-to-db', methods=['POST'])
def send_to_db():
    """Recibe un valor int y lo envía a InfluxDB."""
    data = request.get_data(as_text=True)

    # Validar que el parámetro sea int
    try:
        valor = int(data)
    except (ValueError, TypeError):
        return jsonify({"error": "El valor debe ser un entero"}), 400

    # Enviar a InfluxDB
    if enviar_influx(valor):
        return jsonify({"message": "Dato enviado correctamente", "valor": valor}), 200
    else:
        return jsonify({"error": "Error al enviar a InfluxDB"}), 500
