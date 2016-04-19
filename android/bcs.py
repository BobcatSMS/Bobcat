#BOBCAT SENDER#
import socket
import android
droid = android.Android() 

BOBCAT_HOST = "192.168.0.22"
BOBCAT_PORT = 5001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((BOBCAT_HOST, BOBCAT_PORT))
s.listen(10)

while True:
	print()
	print('Pending...')
	conn, addr = s.accept()
	print('Entering connection...')

	data = conn.recv(2048)
	print('Received : ', data)
	d = json.loads(data.decode())
	droid.smsSend(d['number'], d['message'])
	print('Sent to', d['number'], ':')
	print(d['message'])

	conn.close()


