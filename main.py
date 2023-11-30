from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
import paho.mqtt.client as mqtt

class PetFeederApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Widget de imagem para representar o estado do compartimento
        self.compartment_image = Image(source='empty.jpg')  # Substitua 'closed.png' pela imagem desejada
        self.layout.add_widget(self.compartment_image)

        # Botões para abrir e fechar o compartimento
        self.button_open = Button(text='Abrir Compartimento')
        self.button_close = Button(text='Fechar Compartimento')

        self.button_open.bind(on_press=self.send_open_command)
        self.button_close.bind(on_press=self.send_close_command)

        self.layout.add_widget(self.button_open)
        self.layout.add_widget(self.button_close)

        # Configurar o cliente MQTT
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.connect("mqtt.eclipseprojects.io", 1883, 60)

        return self.layout

    def send_open_command(self, instance):
        self.send_mqtt_command("abrir")

    def send_close_command(self, instance):
        self.send_mqtt_command("fechar")

    def send_mqtt_command(self, command):
        topic = "pet_feeder/control"
        self.client.publish(topic, command)

    def on_connect(self, client, userdata, flags, rc):
        print("Conectado com código de resultado: " + str(rc))

    def on_publish(self, client, userdata, mid):
        print("Abrindo alimentador...")

        # Atualizar a imagem com base no estado do compartimento
        if client.publish(topic="pet_feeder/control", payload="status", qos=1, retain=True):
            print(client)
            teste = True
            if teste:
                self.compartment_image.source = 'full.jpg'
                teste = False
            # Substitua 'open.png' pela imagem desejada quando o compartimento estiver aberto
            else:
                self.compartment_image.source = 'empty.jpg'  # Substitua 'closed.png' pela imagem desejada quando o compartimento estiver fechado
            print(teste)
if __name__ == '__main__':
    PetFeederApp().run()