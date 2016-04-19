import json
import subprocess
import applications.application as a
import data.model

db = data.model.Model("bobcat", "bobcat", "bobcat")

class Fleas:
    """Identifers management"""

    def is_valid(identifier):
        return True
    
    def get_send_command(identifier):
        """return the command that subprocess needs"""
        return 'python3'

    def get_type(identifier):
        r = db.sql("select type from fleas WHERE id = "+str(identifier))[0][0]
        if not r:
            raise Exception('Invalid type identifier')
        return r



class BobMessage:
    """
    A bobcat message.
    Sender and receiver must be valid Fleas.
    BobMessage example :
    {
        'sender' : '00000001'   //id unique (sender number + app id)
        'receiver' : 'meteo'
        'message' : 'Valence'
    }
    """

    def __init__(self, string = '{}'):
        self.data = json.loads(string)

    def __str__(self):
        return json.dumps(self.data)

    def is_valid(self):
        return (Fleas.is_valid(self.data['receiver']) and Fleas.is_valid(self.data['sender']))

    def send(self):
        print('send received', str(self))
        if Fleas.get_type(self.data['receiver']) == 'app':
            subprocess.run(
            [
                Fleas.get_send_command(self.get_receiver()),    #example : python3
                "applications/"+str(self.get_receiver())+"/main.py", 
                a.ON_SMS,
                self.data['command'],
                self.__str__()
            ])
        elif Fleas.get_type(self.data['receiver']) == 'sms':
            subprocess.run(['python3', 'reversoSmsOut.py', self.__str__()])

    def get_sender(self):
        return self.data["sender"]

    def get_receiver(self):
        return self.data["receiver"]

    def get_content(self):
        return self.data['message']

    def set_sender(self, sender):
        self.data["sender"] = str(sender)

    def set_receiver(self, receiver):
        self.data["receiver"] = str(receiver)

    def set_content(self, message ):
        self.data["message"] = str(message)
