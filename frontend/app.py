import sys
from flask import Flask, render_template
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

_my_uuid = ""

# Define the MQTT client and callbacks
client = mqtt.Client(client_id="", userdata=None, protocol=mqtt.MQTTv5)

def on_connect(client, userdata, flags, rc, properties=None):
    print("MQTT broker connected!")
    client.subscribe("taugroup/{uuid}".format(uuid=_my_uuid), qos=1)

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Topic subscribed!")

def on_message(client, userdata, msg):
    print(msg.topic + ":\t" + str(msg.payload))
    # Send the message to the connected WebSocket clients
    socketio.emit('mqtt_message', {'topic': msg.topic, 'payload': str(msg.payload)})



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

    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "-topic":
            _my_uuid = sys.argv[2] 
    else:
        _my_uuid = "smart_farm"

    print(_my_uuid)

    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    client.username_pw_set("taugroup", "TAUGroup2023")
    client.connect("385660998355465faf56ba893a544dcf.s1.eu.hivemq.cloud", 8883)

    client.loop_start()
    socketio.run(app, host='127.0.0.1', port=5000)
