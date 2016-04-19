import bobcat as b
import sys

if __name__ == '__main__':
	message = b.BobMessage(sys.argv[1])

	if not message.is_valid():
		raise Exception("This Message isn't a Valid BobMessage : " + message)
	message.send()
