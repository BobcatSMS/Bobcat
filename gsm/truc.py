text = "zeub"
hexa = ""
for i in text:
    hexa += str(hex(ord(i)))[2:].zfill(4)
print(hexa)



hexa = "002B00330033003600380039003000300034003000300030" #YOLOO
hexa = [hexa[i:i+4] for i in range(0, len(hexa), 4)]
text=""
for i in hexa:
    text+=chr(int(i, 16))
print(text)