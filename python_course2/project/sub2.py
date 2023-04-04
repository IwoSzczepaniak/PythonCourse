import paho.mqtt.client as mqtt
import pyttsx3
import tkinter as tk

# Initialize TTS engine
engine = pyttsx3.init()

# Initialize MQTT client
client = mqtt.Client()

# MQTT server address and port
broker_address = "localhost"
port = 1883

# MQTT topic to subscribe to
speak_topic = "msg/spk"

Texts = []

# Function to handle receiving messages on the "msg/spk" topic
def on_message(client, userdata, message):
    # Read the text from the MQTT message
    text = message.payload.decode()
    Texts.append(text)

# Configure MQTT client and establish connection
client.on_message = on_message
client.connect(broker_address, port=port)
client.subscribe(speak_topic)

def say(text):
    engine.say(text)
    engine.runAndWait()

# Function to handle button click
def on_button_click():
    if len(Texts) > 0:
        say("Oto nagrane wiadomości.")
        for i, text in enumerate(Texts):
            say(f"Wiadomość: {i+1}:")
            say(text)
        say("Koniec wiadomości.")
    else:
        say("Brak wiadomości")

# Create main window
root = tk.Tk()

label = tk.Label(text="Naciśnij przycisk aby odsłuchać wiadomości:")
label.pack()

# Add button to window
button = tk.Button(root, text="Odłuchaj!", command=on_button_click)
button.pack()

# Start MQTT client loop
client.loop_start()

# Start main window loop
root.mainloop()

# Stop MQTT client loop
client.loop_stop()
