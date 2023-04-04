import paho.mqtt.client as mqtt

client = mqtt.Client()

broker_address = "localhost"
port = 1883

mic_topic = "msg/spk"

def send_message(text):
    client.connect(broker_address, port=port)
    client.publish(mic_topic, text)
    client.disconnect()

send_message("Hello World!")
send_message("HI")