# 프로젝트 개요

```
해당 프로젝트의 최종 목표는 홈 IOT 플랫폼을 구성하는 것 입니다.
그러기 위해서 IOT 장비에서 MQTT 로 데이터를 Host PC 의 MongoDB 로 보내고,
해당 데이터를 필요에 맞게 가공하여 서비스를 집에 있는 월패드(Android Tablet)를 통해 제공해야 됩니다.

단계별로 진행되며, 첫단계인 이 Repository 에서는 해당 서비스의 기본적인 이해를 위해 
Anroid Phone -> MQTT -> HostPC -> MongoDB 형태로 구축해보겠습니다.
```

## 1. MQTT 를 Host PC 에 세팅 (ubuntu)

```
Broker Mosquitto 설치 
$ sudo apt install mosquitto

Mosquitto 서비스 실행
$ sudo systemctl status mosquitto.service

Publish, Subscribe 할 수 있게 client 설치
$ sudo apt install mosquitto-clients
```

## 2. Android 폰에 MQTT 연결

```
build.gradle(Module: app) 의 dependcies 에 하기 두 줄 추가.

implementation 'org.eclipse.paho:org.eclipse.paho.client.mqttv3:1.2.2'
implementation 'org.eclipse.paho:org.eclipse.paho.android.service:1.1.1'

-> service 가 제대로 안된다고 오류가 뜨는 경우, 먼저 버전을 낮추어서 해주고, 다시 1.1.1 로 해주니 되었습니다.
-> 버전이 같아야지 제가 올린 MainActivity.java 의 코드와 완전히 호환됩니다.  

AndroidManifest.xml 에 permission 과 service 등록

<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.WAKE_LOCK" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

<service android:name="org.eclipse.paho.android.service.MqttService" />

마지막으로 MainActivity.java 와 activity_main.xml 코드를 복사해 붙여넣으면 아래와 같은 앱 화면으로 됩니다.

MainActivity.java 의 하기 32 번째 줄
mqttAndroidClient = new MqttAndroidClient(this,  "tcp://" + "192.168.20.184" + ":1883", MqttClient.generateClientId());
에서 "192.168.20.184" + ":1883" 은 ip 주소와 port 번호로 사용하시는 본인의 ip 와 port 에 맞게 설정하시면 됩니다.
Ubuntu 의 경우 ifconfig 를 하면 ip 주소를 확인할 수 있습니다.
```
<img src="https://github.com/Taehyung93/mqtt_mongodb/blob/master/Mqtt_android.jpg" width="30%" height="30%" title="anroid_mqtt" alt="android_mqtt"></img>

## 3. Mongodb 설치 (ubuntu)

```
Host PC 에서 하기 링크로 들어가서 순서대로 진행하면 mongodb 가 잘 설치됩니다.

https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

정상적으로 설치되었다면 하기 코드로 실행이 됩니다.

$ sudo service mongod start

기본 포트는 27017 이며, 방화벽을 사용한다면 해당 포트를 open 해줘야 됩니다.

mongodb client terminal 접속
$ mongo

db 생성 -> 이미 생성된 후에는 똑같이 치면 이미 만들어진 db로 연결이 된다.
$ use mongo_test

collection 생성
$ db.createCollection("mongo_test")

아래 python script 에서 바로 따로 코드 변경없이 사용하려면(ip 제외), db 명과 collection 명을 똑같이 입력해주세요.
```

## 4. Python Subscribe 코드 설정

```
업로드되어있는 subscribe.py 다운해주시고, ip 를 본인의 Host PC 에 맞게 변경해줘야됩니다.

import paho.mqtt.client as mqtt 는 mqtt 와 python 을 연결시켜주는 라이브러리이고,
import pymongo 는 mongodb 와 python 을 연결시켜주는 라이브러리 입니다.

간단하므로 따로 더 코드 설명을 드리지 않겠습니다.
```

## 5. 실행 

```
주의! Android 폰의 네트워크와 HostPC 의 네트워크는 같은 망을 사용해야지만 제대로 동작됩니다.
그렇지 않고 사용하려면 포트포워딩된 네트워크를 Host PC 에서 사용을 하던가, AWS 같은 서버에 MQTT 서버와 Mongodb 를 업로드해야됩니다.

Host PC 에서 Mosquitto subscribe 생성
$ mosquitto_sub -h 192.168.20.184 -t test
- 192.168.20.184 는 제 개인 컴퓨터의 IP 입니다. 127.0.0.1 로 하면 Android 폰에서 접근을 할 수 없습니다.
- -t 뒤의 test 는 topic name 입니다.

Host PC 에서 Python script 실행
$ python3 subscribe.py
-> 해당 subscribe.py 의 마지막 줄인 client.loop_forever() 에 의해 터미널에서 직접 꺼줄 때까지 계속 실행중입니다.

Android 폰에서 온도를 입력하고 전송 버튼 클릭
-> python 및 mosquitto 터미널에 해당 값이 올라오는 것을 확인

mogodb 접속
$ mongo
$ use mongo_test
하기 코드로 전송한 온도 값이 들어온 것을 확인
$ db.test_table.find() 

```

## 6. 기타 

```
Mosquitto publish 방법
$ mosquitto_pub -h 192.168.20.184 -t test -m "Hello Mosquitto !"

subscribe.py -> multiple msg 를 전송할 수 있다.

Mongodb 시각화 무료 어플리케이션(오픈소스): Robo 3T 
설치방법 링크: https://tinyurl.com/yasbqev5

pymongo 기초 사용법 : https://brownbears.tistory.com/282
```
