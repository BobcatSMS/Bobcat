import time
import serial

recipient = "+33604431630"  #JuL
message = "Celui qui lit ca et un con"
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=5)

try:
    print("AT -------------")
    time.sleep(0.5)
    ser.write("AT\r")
    response =  ser.read(5)
    print(response)
    
    print("ATZ-------------")
    time.sleep(0.5)
    ser.write("ATZ\r")
    response =  ser.read(5)
    print(response)
    
    print("CMGF =1-------------")
    time.sleep(0.5)
    ser.write("AT+CMGF=1\r")
    response =  ser.read(5)
    print(response)
   
    print("CMGS 1-------------")
    time.sleep(0.5)
    ser.write('AT+CMGS="0033003300360030003400340033003100360033003",145'+"\r")
    #ser.write(b'AT+CMGS="' + recipient.encode() + b'"\r')
    response =  ser.read(5)
    print(response)
    
    print("CMGS 2-------------")
    time.sleep(3)
    ser.write("007a006500750062001a")
    #ser.write(message.encode() + b"\r")
    response =  ser.read(5)
    print(response)
    time.sleep(0.5)
    #ser.write(bytes([26]))  #ser.write(chr(26))
    #response =  ser.read(2)
    #print(response)
    time.sleep(0.5)
finally:
    ser.close()