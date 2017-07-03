#!/usr/bin/env python
from flask import Flask, render_template, session, request, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import paho.mqtt.client as mqtt
import json
import math
from threading import Thread


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__, ) 
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

count = 0

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('my_event', namespace='/test')
def test_message(message):
    print("my_event!!!!")
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})

@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    # global thread
    # if thread is None:
    #     thread = socketio.start_background_task(target=background_thread)
    mqtt_thread = MQTT_Thread()
    mqtt_thread.start()
    print("Mqtt STart!!!!!!!!!")   
    emit('my_response', {'data': 'Connected', 'count': 0})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


#########################################################################

def on_connect(client, userdata, rc):
    print("on_connect:[{0}]".format(str(rc)))
    client.subscribe("#")

def on_message(client, userdata, message):
    print("on_message")
    print("payload: %s" % message.payload)

    raw = message.payload.decode()
    if socketio is not None:
        print("emit socket io")
        socketio.emit('my_response',{'data': 'Server generated event', 'count': count},namespace='/test')

    raw_len=len(raw)
    print(raw)
    #socketio.emit('my_response',{'rssi':int(rssi,16)-128 ,'minor': int(minor), 'sta': dic_msg['sta']},namespace='/test')

def on_disconnect(client, userdata, rc):
  if rc != 0:
    print("Desconexion inesperada al servidor MQTT COD:[{0}]".format(str(rc)))



class MQTT_Thread(Thread):
  def __init__(self):
    Thread.__init__(self)
    self.stop = False

  def run(self):
    print("Thread Run!!!!!!!!")
    while not self.stop and client.loop_forever() == 0:
      pass
    print("MQTT Thread terminado")

client = mqtt.Client(client_id="agente")
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883)
client.subscribe("#")

 

if __name__ == '__main__':
    socketio.run(app, debug=False,host='0.0.0.0')



