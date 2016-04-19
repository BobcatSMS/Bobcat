import sys
import json
import subprocess
import socket
import data.model
import logging


db = data.model.Model('bobcat', 'bobcat', 'bobcat')


def parse_sms(sms):
	sms_text = json.loads(sms.decode())
	print('Reverso recveived', sms_text)
	sms_words = sms_text['message'].split()
	receiver = db.getAppID(sms_words[0].lower())
	sender = db.getUniqueUserID(db.getUserId(sms_text['number']), receiver)
	print('reversoin', db.getUserId(sms_text['number']), receiver)
	message = ' '.join(sms_words[1:])

	return json.dumps({"sender" : sender, "receiver" : receiver, "message": message, "command":sms_words[0].lower()})


logging.basicConfig(filename='log/reversoSmsIn.log',level=logging.DEBUG)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logging.debug("Socket created")

try:
	s.bind(('', 5000))
	logging.debug("Socket ready")
except:
	logging.error("Fail binding")
	sys.exit()

s.listen(10)
logging.debug("Socket listening")


while True:
	logging.debug("Waiting for connection")
	conn, addr = s.accept()
	logging.debug("Accepted from " + str(addr))
	while True:
		data = conn.recv(1024)
		if not data:
			break

		logging.debug('Received : '+ str(data))
		subprocess.run(["python3", "main.py", parse_sms(data)])

	conn.close()
s.close()
