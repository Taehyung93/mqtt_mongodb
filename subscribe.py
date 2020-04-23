import paho.mqtt.client as mqtt
import pymongo

conn = pymongo.MongoClient('127.0.0.1', 27017) # mongoDB에서 port를 변경하지 않았으면 기본값인 27017
db = conn.get_database('mongo_test') # mongo_test 데이터베이스 선택
collection = db.get_collection('test_table') # test_table 테이블 선택

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("test") 

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(str(msg.payload).split("\'")[1])
	collection.insert({"temp":int(str(msg.payload).split("\'")[1])})

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.20.184") # - 서버 IP '테스트를 위해 test.mosquitto.org'로 지정

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
