'''
    Mosquitto consumer. Read message from message queue new_prediction and save
    the data in the database.
'''
import paho.mqtt.client as mqtt
from application import Application
from data_models import Prediction

app = Application.get_instance()
app.init_db()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('new_prediction')


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print('New message: %s' % msg.payload)
    Prediction.create_from_mq(msg.payload)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('mosquitto', 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
