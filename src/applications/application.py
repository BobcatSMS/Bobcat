import sys
sys.path.append('/'.join(sys.path[0].split('/')[0:-2]))
import data.model
import subprocess
import json
import logging


"""
Structure of an app:



import sys
sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
import application as a

class YourApplication:

	def on_SMS(self, data):
		# TO BE IMPLEMENTED
		# Called when an SMS is received by the application.
		# data : dictionnary cotaining the following keys :
		#	["sender"] : the unique ID of the user for this app
		#	["receiver"] : the ID of this app (?) (should contain the command used ?) #TODO #YOUDECIDE
		#	["message"] : content of the message (without the first word) (this key may not exist)
		#	
		#
		#

	def on_wake_up(self, reason):
		#TO BE IMPLEMENTED

a.init(YourApplication())		# Calls the right method according to the event
"""




###############################
## APPLICATION-CALLING TYPES ##
###############################
ON_SMS = "on_sms"
ON_WAKEUP = "on_wake_up"
ON_INSTALL = "on_install"
ON_USER_WEB_ACCESS = "on_user_web_access"
ON_ADMIN_WEB_ACCESS = "on_admin_web_access"
ON_PUBLIC_WEB_ACCESS = "on_public_web_access"

###############################
## CALLING THE RIGHT INIT METHOD AND SAVING THE APP ID 
###############################

sender = 0

def init(caller, id):
	onType = sys.argv[1]

	global sender
	sender = id
	#TODO path
	#logging.basicConfig(filename='log/reversoSmsIn.log',level=logging.DEBUG)


	if onType == ON_SMS:
		caller.on_SMS(sys.argv[2], json.loads(sys.argv[3]))

	elif onType == ON_WAKEUP:
		caller.on_wake_up(sys.argv[2])

	elif onType == ON_INSTALL:
		caller.on_install()

	elif onType == ON_USER_WEB_ACCESS:
		unique_id = data.model.Model("bobcat", "bobcat", "bobcat").getUniqueUserID(sys.argv[2], id)
		caller.on_user_web_access(unique_id, json.loads(sys.argv[3]), json.loads(sys.argv[4]))

	elif onType == ON_ADMIN_WEB_ACCESS:
		unique_id = data.model.Model("bobcat", "bobcat", "bobcat").getUniqueUserID(sys.argv[2], id)
		caller.on_admin_web_access(unique_id, json.loads(sys.argv[3]), json.loads(sys.argv[4]))
	
	elif onType == ON_PUBLIC_WEB_ACCESS:
		unique_id = data.model.Model("bobcat", "bobcat", "bobcat").getUniqueUserID(sys.argv[2], id)
		caller.on_public_web_access(unique_id, json.loads(sys.argv[3]), json.loads(sys.argv[4]))
	
	else:
		print('arg error')

###############################
##      CALLABLE METHODS     ##
###############################
def send_message(receiver, message_content):
	message = json.dumps({
	"sender" : sender,
	"receiver" : receiver,
	"message" : message_content
	})
	print('application send received', message)
	subprocess.run(['python3', "reversoSmsOut.py", message])


def get_db():
	return data.model.Model(username="bobcat_"+str(sender), password="bobcat_"+str(sender), dbname="bobcat_"+str(sender))

def get_url():
	return '/?page=application&s='+str(sender)

def p(string):
	sys.stdout.write(string)

# def log(level='debug', message):
# 	if level == 'debug':
# 		pass

