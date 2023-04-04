import paho.mqtt.client as mqtt
import pyttsx3

engine = pyttsx3.init()

client = mqtt.Client()

broker_address = "localhost"
port = 1883

speak_topic = "msg/spk"

def on_message(client, userdata, message):
    text = message.payload.decode()
    engine.say(text)
    engine.runAndWait()

client.on_message = on_message
client.connect(broker_address, port=port)
client.subscribe(speak_topic)

client.loop_forever()
