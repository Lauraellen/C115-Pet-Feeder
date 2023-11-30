from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
import paho.mqtt.client as mqtt

class PetFeederApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Widget de imagem para representar o estado do compartimento
        self.compartment_image = Image(source='empty.jpg')
        self.layout.add_widget(self.compartment_image)

        # Botão para abrir o compartimento
        self.button_open = Button(text='Abrir Compartimento')
        self.button_open.bind(on_press=self.send_open_command)
        self.layout.add_widget(self.button_open)

        # Configurar o cliente MQTT
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.connect("mqtt.eclipseprojects.io", 1883, 60)

        return self.layout

    def send_open_command(self, instance):
        self.send_mqtt_command("abrir")

    def send_mqtt_command(self, command):
        topic = "pet_feeder/control"
        self.client.publish(topic, command)

    def on_connect(self, client, userdata, flags, rc):
        print("Conectado com código de resultado: " + str(rc))

    def on_publish(self, client, userdata, mid):
        print("Abrindo alimentador...")

        # Atualizar a imagem com base no estado do compartimento
        self.compartment_image.source = 'full.jpg'

        # Agendar a reversão da imagem para o estado vazio após 5 segundos
        Clock.schedule_once(self.restore_empty_image, 3)

    def restore_empty_image(self, dt):
        print("Fechando compartimento...")
        self.compartment_image.source = 'empty.jpg'

if __name__ == '__main__':
    PetFeederApp().run()
