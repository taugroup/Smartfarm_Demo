from flask import Flask, render_template
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

# Define the MQTT client and callbacks
client = mqtt.Client(client_id="", userdata=None, protocol=mqtt.MQTTv5)

def on_connect(client, userdata, flags, rc, properties=None):
    print("MQTT broker connected!")
   # client.subscribe("taugroup/beef_center", qos=1)
    client.subscribe("taugroup/smart_farm", qos=1)

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Topic subscribed!")

def on_message(client, userdata, msg):
    print(msg.topic + ":\t" + str(msg.payload))
    # Send the message to the connected WebSocket clients
    socketio.emit('mqtt_message', {'topic': msg.topic, 'payload': str(msg.payload)})

client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message

client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set("nistai3", "nistpscrai3")
client.connect("030a29b11d714f4dae6fb60c9ab4a2c5.s1.eu.hivemq.cloud", 8883)

# Define the route for the HTML page
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def socket_connect():
    print('WebSocket client connected')

@socketio.on('disconnect')
def socket_disconnect():
    print('WebSocket client disconnected')

# Run the Flask application with SocketIO
if __name__ == '__main__':
    client.loop_start()
    socketio.run(app, host='127.0.0.1', port=5000,allow_unsafe_werkzeug=True)


# google colab, ngrock