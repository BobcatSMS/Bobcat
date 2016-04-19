import serial
import time
import binascii

ser= serial.Serial('/dev/ttyUSB0',115200,timeout=2)
ser.write("ATZ\r")
time.sleep(1)
ser.write("AT+CMGF=1\r")
response=ser.read(8000)
response =""


while(1):
	print("---------------")	
	ser.write("AT+CMGL=\"REC UNREAD\"\r")
	response=ser.read(8000)
	responsTab = response.split("\n")+["","",""]
	if responsTab[3] != "":
		num = (responsTab[1].split(","))[2]

		st=num[1:-1]
		st = [st[i:i+4] for i in range(0, len(st), 4)]
		stt=""
		for i in st:
		    stt+=chr(int(i, 16))
		print(stt)	
		
		st=str(responsTab[2])
		st = [st[i:i+4] for i in range(0, len(st), 4)]
		stt=""
		for i in st:
			if i != "" and i != "\r":
				stt+=chr(int(i, 16))
		print(stt)
		
		

		#print responsTab[3]
	#print(type(response))
	#print(response)
	


# stt = binascii.hexlify(u"YOLOO".encode('utf-8'))
# print(stt)




#ser.write(("AT+CMGL=\"STO SENT\"\r").encode())
#response=ser.read(60)
#print(response)

#ser.write(("AT+CMGS=\"+33604431630\"\r"))
#time.sleep(1)
#ser.write(("balakkazeazelaze\r\n"))
#ser.write(chr(26))
#response=ser.read()
#print(response)
ser.close()
