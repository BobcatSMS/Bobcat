import sys
sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
import application as a
import random as r

class Dice:
	"""
	Dice
	"""

	def on_SMS(self, command, data):

		if command == "dice" :
			try:
				i = int(data["message"])
			except :
				i = 6
			a.send_message(data["sender"], "Roll... Result : "+str(r.randint(1,i)))
			exit()

		if command == "mdice" : # usage mdice nbdice max
			m_split = data["message"].split()
			try:
				i = int(m_split[0])
			except :
				i = 6
			try:
				j =  int(m_split[1])
			except :
				j = 1
			res = [str(r.randint(1,i)) for k in range (0,j)]
			res_string = " ".join(res)
			a.send_message(data["sender"], "Roll... Result : "+ res_string)
			exit()

	def on_wake_up(self, reason): ## TODO ERASE IT'S CONFIG FOR DEBUG
		pass

	def on_install(self):
		pass;

	def on_user_web_access(self, user_id, get_array, post_array):
		pass

	def on_admin_web_access(self, user_id, get_array, post_array):
		pass

	def on_public_web_access(self, user_id, get_array, post_array):
		    a.p("""
            <p>Alea jacta est !</p>
            <h4>Commands</h4>
            <p><span class="label label-primary">dice</span> <span class="label label-info">faces</span> : roll a dice.</p>
            <p><span class="label label-primary">mdice</span> <span class="label label-info">faces</span> <span class="label label-info">rolls</span> : roll several dices.</p>
            """)

a.init(Dice(), 78)
