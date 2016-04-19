import sys
import json
import data.model
import socket

db = data.model.Model('bobcat', 'bobcat', 'bobcat')

PHONE_HOST = "192.168.0.17"
PHONE_PORT = 5001
DEBUG_DIAL = "+33604431630"

data = json.loads(sys.argv[1])
print('out received',data)
msg={}
msg['number'] = db.getPhoneNumber(data['receiver'])
msg['message'] = data['message']

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((PHONE_HOST, PHONE_PORT))

s.send(json.dumps(msg).encode())

print("SMS from", data["sender"], "to", data["receiver"], "(", db.getPhoneNumber(data["receiver"]), ")", ":")

s.close()
