import sys
sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
import application as a
import json

class Ping:
	"""
	Ping
	"""

	def on_SMS(self, command, data):
		a.send_message(data["sender"], "Désolé, nous ne connaissons pas la commande \""+data['command']+"\" !")

	def on_wake_up(self, reason):
		pass

	def on_user_web_access(self, user_id, data):
		print(data)
		print('<form method="post" action=""><p>Bonjour<p><input type="text" name="name" /><input type="submit" /></form>')


	def on_admin_web_access(self, user_id, data):
		print("Bonjour, monsieur l'admin")


a.init(Ping(), 15)
