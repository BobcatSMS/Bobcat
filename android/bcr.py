#BOBCAT RECEIVER#
import android
import time
import socket
import json
import datetime
 
BOBCAT_HOST = "192.168.0.22"
BOBCAT_PORT = 5000
 
droid = android.Android()
 
while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    print("Waiting for server...")
    c = False
   
    while sock.connect_ex((BOBCAT_HOST, BOBCAT_PORT)):
        pass
       
 
    print("-- Connected --")
    while True :
        try:
            sock.recv(1024)
            sock.close()
            break
        except:
            pass
           
        new_sms = droid.smsGetMessageIds(True).result
        for sms in new_sms :
            s = droid.smsGetMessageById(sms).result
            datesms = datetime.datetime.fromtimestamp(int(s['date'])//1000).strftime('%d/%m/%Y %H:%M:%S')
            print()
            print(datesms + ' [' + s['address'] + ']')
            print(s['body'])
            msg = json.dumps({"number" : s['address'], "message" : s['body']}).encode()
            sock.send(bytes(msg))
        droid.smsMarkMessageRead(new_sms, 1)
        time.sleep(1)
    print()
    print("-- Disconnected --")
    