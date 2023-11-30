import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Conectado com código de resultado: " + str(rc))

def on_publish(client, userdata, mid):
    print("Abrindo alimentador")

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

client.connect("mqtt.eclipseprojects.io", 1883, 60)

# Simulação de abrir o compartimento
client.publish("pet_feeder/control", "abrir")
time.sleep(5)  # Aguarda 2 segundos

# Simulação de fechar o compartimento
client.publish("pet_feeder/control", "fechar")

client.disconnect()
