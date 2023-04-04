import paho.mqtt.client as mqtt
import speech_recognition as sr
import tkinter as tk

client = mqtt.Client()

broker_address = "localhost"
port = 1883

# Stały temat MQTT
mic_topic = "msg/spk"

def send_message(text):
    client.connect(broker_address, port=port)
    client.publish(mic_topic, text)
    client.disconnect()

def get_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        r.energy_threshold = 100  # Set the energy threshold to 500
        print("Słucham...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language='pl-PL')
        print("Rozpoznano: " + text)
        return text
    except sr.UnknownValueError:
        print("Nie udało się rozpoznać mowy")
        send_message("Nie udało się rozpoznać mowy")
    except sr.RequestError as e:
        print("Błąd serwera Google: {0}".format(e))

def send_text():
    text = get_text()
    if text:
        send_message(text)

window = tk.Tk()
window.title("Sender")

label = tk.Label(text="Naciśnij przycisk aby wysłać wiadomość:")
label.pack()

button = tk.Button(text="Nasłuchuj i wyślij", command=send_text)
button.pack()

window.mainloop()
