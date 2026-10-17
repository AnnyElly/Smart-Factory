# CP06 - Smart Factory

**Disciplina:** Edge Computing | **Turma:** 2CCPG 
**Integrantes:** Anny Elly Pantoja Martin | **RM:**565055

- Wokwi: https://wokwi.com/projects/478144141487420417
- Vídeo do youtube: https://youtu.be/RyeMu1js5p4
- Tópico MQTT: o meu computador não e compativel ao docker

## Arquitetura
ESP32 → HiveMQ (broker.hivemq.com:1883) → API Flask (:5000) → Dashboard Flask (:5001)

- **Processamento local (borda):** o ESP32 lê o DHT22, decide NORMAL/ALERTA (> 35 °C) e controla os LEDs sem depender de API ou dashboard.
- **HiveMQ:** apenas transporta as mensagens.
- **API:** assina o tópico e guarda a última leitura.
- **Dashboard:** o backend consulta `http://api:5000/dados` e exibe temperatura, umidade e estado.


## Testes
Sequência 30 → 35 → 36 → 30 °C: NORMAL → NORMAL → ALERTA → NORMAL.

