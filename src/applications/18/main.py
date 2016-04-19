import sys
sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
import application as a

class Citation:
	"""
	Citation
	"""

	def on_SMS(self, command, data):
		a.send_message(data["sender"], "« Ad augusta per angusta »")

	def on_wake_up(self, reason):
		pass

	def on_install(self):
		pass;

	def on_user_web_access(self, user_id, get_array, post_array):
		pass

	def on_admin_web_access(self, user_id, get_array, post_array):
		pass

	def on_public_web_access(self, user_id, get_array, post_array):
		    a.p("""
            <p class="alert alert-warning"> <strong>Warning!</strong> Still under development : for now always return the same quote.</p>
            <h4>Commands</h4>
            <p><span class="label label-primary">citation</span> : get a random citation.</p>
            """)
           


a.init(Citation(), 18)
