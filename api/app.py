import json
import os
import threading

import paho.mqtt.client as mqtt
from flask import Flask, jsonify

MQTT_HOST = "broker.hivemq.com"
MQTT_PORT = 1883
# Deve ser IGUAL ao tópico do ESP32. Pode ser sobrescrito pela variável MQTT_TOPIC.
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "edge/2ano/2cc/equipe07/x9k3q2/dados")
MQTT_CLIENT_ID = "api-smartfactory-equipe07-x9k3q2"  # diferente do ESP32

app = Flask(__name__)

ultima_leitura = None
lock = threading.Lock()


def eh_numero(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"[MQTT] Conectado ({reason_code}). Assinando {MQTT_TOPIC}", flush=True)
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    global ultima_leitura
    try:
        dados = json.loads(msg.payload.decode("utf-8"))
        temperatura = dados["temperatura"]
        umidade = dados["umidade"]
        estado = dados["estado"]
        if not (eh_numero(temperatura) and eh_numero(umidade)
                and estado in ("NORMAL", "ALERTA")):
            raise ValueError("campos inválidos")
    except (ValueError, KeyError, TypeError) as e:
        print(f"[MQTT] Mensagem ignorada: {e}", flush=True)
        return

    with lock:
        ultima_leitura = {
            "temperatura": float(temperatura),
            "umidade": float(umidade),
            "estado": estado,
        }
    print(f"[MQTT] Recebido: {ultima_leitura}", flush=True)


def iniciar_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=MQTT_CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    client.reconnect_delay_set(min_delay=1, max_delay=10)
    client.connect_async(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_start()


@app.get("/dados")
def dados():
    with lock:
        leitura = ultima_leitura
    if leitura is None:
        return jsonify({"mensagem": "Aguardando dados do ESP32"}), 503
    return jsonify(leitura), 200


iniciar_mqtt()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)