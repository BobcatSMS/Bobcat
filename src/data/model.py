import psycopg2
import random as r
import re

class Model:
	def __init__(self, dbname, username, password):
		self.username = username
		self.id = username.split('_')[1] if username != 'bobcat' else 0

		try:
			self.conn = psycopg2.connect("dbname='"+dbname+"' user='"+username+"' host='localhost' password='"+password+"'")	
		except:
			print('Database connection error.')
			exit()	

		self.cursor = self.conn.cursor()


	def sql(self, request, params=tuple()):
		cursor = self.conn.cursor()
		cursor.execute(request, tuple(re.escape(x) for x in params))
		try:
			r = cursor.fetchall()	
			cursor.close()
			self.commit()
			return r
		except psycopg2.ProgrammingError:
			pass
		cursor.close()

	def commit(self):
		self.conn.commit()

	def getAppID(self, app):
		"""
		app : a string containing a command. (the first word of an SMS)
		returns the app ID.
		"""
		
		r = self.sql("SELECT application_id FROM commands WHERE value = %s", (app,))
		if r == []:
			return 15
		return r[0][0]

	def getUserId(self, phone_number):
		r = self.sql("SELECT flea_id FROM users WHERE phone_number = '"+phone_number+"'")
		if r == []:
			self.sql("INSERT INTO fleas(type) VALUES('user')")
			id = self.sql("SELECT lastval()")[0][0]
			self.sql("INSERT INTO users(flea_id, phone_number, role) VALUES("+str(id)+",'"+phone_number+"', 'user')")
			return id
		return r[0][0]

	def getUniqueUserID(self, user_id, app_id):
		"""
		phone_number : an actual phone number
		app_id : an app ID
		returns the unique user-app ID.
		"""

		unique = self.sql("SELECT uniqueid FROM applications_users WHERE user_id = %s AND application_id = %s;", (str(user_id), str(app_id)))
		if unique == []:
			unique = self.sql("INSERT INTO applications_users(user_id, application_id, uniqueid) VALUES(%s, %s, %s)", (str(user_id), str(app_id), str(r.randint(100000000, 999999999))))	
			unique = self.sql("SELECT uniqueid FROM applications_users WHERE user_id = %s AND application_id = %s;", (str(user_id), str(app_id)))
		return unique[0][0]


	def getPhoneNumber(self, uniqueid):
		r = self.sql("SELECT phone_number FROM users INNER JOIN applications_users ON users.flea_id = applications_users.user_id WHERE uniqueid = %s;", (str(uniqueid),))
		if r == []:
			return None
		return r[0][0]

	def get_slug_by_id(self, id):
		r = self.sql("SELECT slug FROM applications WHERE flea_id = %s", (str(id),))
		if r == []:
			return id
		return r[0][0]
