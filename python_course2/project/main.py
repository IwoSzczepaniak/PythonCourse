import tkinter as tk
import paho.mqtt.client as mqtt

# ustalenie stałych tematów
SUB_TOPIC = "msg/spk"
PUB_TOPIC = "msg/mic"

# funkcja wywoływana po otrzymaniu wiadomości
def on_message(client, userdata, msg):
    # wypowiedzenie otrzymanej wiadomości
    message = msg.payload.decode()
    message_listbox.insert(tk.END, message)

# funkcja wywoływana po wciśnięciu przycisku "Wyślij"
def send_message():
    # pobranie tekstu z pola tekstowego
    message = message_entry.get()
    # zamiana tekstu na słowa oddzielone spacjami
    words = message.split()
    # wygenerowanie komunikatu w formacie "word1/word2/word3/..."
    payload = "/".join(words)
    # wysłanie komunikatu do serwera MQTT
    client.publish(PUB_TOPIC, payload)

# utworzenie klienta MQTT i połączenie z brokerem
client = mqtt.Client()
client.connect("localhost", 1883)

# ustawienie funkcji obsługi otrzymanych wiadomości
client.on_message = on_message

# subskrypcja na temat SUB_TOPIC
client.subscribe(SUB_TOPIC)

# utworzenie interfejsu użytkownika
root = tk.Tk()

# pole tekstowe do wprowadzania wiadomości
message_entry = tk.Entry(root, width=50)
message_entry.pack()

# przycisk do wysyłania wiadomości
send_button = tk.Button(root, text="Wyślij", command=send_message)
send_button.pack()

# pole tekstowe wyświetlające otrzymane wiadomości
message_listbox = tk.Listbox(root, height=10, width=50)
message_listbox.pack()

# rozpoczęcie nasłuchiwania na wiadomości MQTT
client.loop_start()

# uruchomienie pętli głównej aplikacji Tkinter
root.mainloop()

# zakończenie nasłuchiwania na wiadomości MQTT
client.loop_stop()
