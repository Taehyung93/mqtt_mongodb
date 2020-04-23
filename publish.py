import paho.mqtt.publish as publish

msgs = \
[
	{
		'topic':"test",
		'payload':"multiple 1"
	},

	(
		"test",
		"multiple 2",0, False
	)
]

publish.multiple(msgs, hostname = "192.168.20.184")

