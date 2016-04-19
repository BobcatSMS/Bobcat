import sys
sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
import application as a
import tweepy as t
import oauth2 as oauth
import urllib.parse as parse


PROXYBC_UNIQUE_ID = 0

consumer_key = 'AZIGodEaOxTEQ7bAnJTTlYJ9z'
consumer_secret = 'qiux32gBP9SAkt1BFbDVGgcNHMPJ39GwUArGJerje72o445aMq'

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'




class TwitterBobcat:
    """
    TwitterBobcat
     {
        'sender' : '00000001'   //id unique (sender number + app id)
        //'receiver' : 'meteo'
        'message' : 'tw xxx'
    }
    """
    def on_SMS(self, command, data):

        

        db = a.get_db()
        
        admin_token = db.sql("SELECT admin_token FROM admin WHERE admin_id = 1;")
        admin_token_secret = db.sql("SELECT admin_token_secret FROM admin WHERE admin_id =1;")
        if admin_token ==[] or admin_token_secret == [] :
            raise Exception("Error, admin not registered")
        auth = t.OAuthHandler(admin_token[0][0], admin_token_secret[0][0]) 


        if command == "twittbc":   
            usr_token = db.sql("SELECT usr_token FROM usr WHERE usr_id ="+ str(PROXYBC_UNIQUE_ID) + ";")
            usr_token_secret = db.sql("SELECT usr_token_secret FROM usr WHERE usr_id ="+ str(PROXYBC_UNIQUE_ID) + ";")
            if usr_token ==[] or usr_token_secret == [] :
                a.send_message(data['sender'], "ERROR.Sorry try again later.")
                raise Exception("Error, @ProxyBc not registered")
                exit()
            auth.set_access_token(usr_token[0][0], usr_token_secret[0][0])          
            api = t.API(auth)
            api.update_status(status=data['message'])
            a.send_message(data['sender'], "Tweet publié sur @ProxyBc !")
            exit()      


        usr_token = db.sql("SELECT usr_token FROM usr WHERE usr_id ="+ str(data["sender"]) + ";")
        usr_token_secret = db.sql("SELECT usr_token_secret FROM usr WHERE usr_id ="+ str(data["sender"]) + ";")
        print('app21', str(data["sender"]), usr_token, usr_token_secret)
        if usr_token ==[] or usr_token_secret == [] :
            a.send_message(data['sender'], "Votre compte twitter n'est pas lié a Bobcat ! @see "+ a.get_url() + ". Utilisez 'Twittbc message' pour publier sur @ProxyBC ")
            exit()
        auth.set_access_token(usr_token[0][0], usr_token_secret[0][0])
        api = t.API(auth)


        if command == "twittlt":
            a.send_message(data['sender'],(api.user_timeline(id=api.get_user(data['message']).id, count = 1)[0].text))
            quit()

        if command == "twitter" :
            api.update_status(data["message"])
            a.send_message(data["sender"], "Tweet publié !")
            quit()
        

    def on_wake_up(self, reason): ## TODO ERASE IT'S CONFIG FOR DEBUG
        pass

    def on_install(self):
        db = a.get_db()
        db.sql("CREATE TABLE usr(usr_id int primary key,usr_token text, usr_token_secret text);")
        db.sql("CREATE TABLE admin(admin_id int primary key,admin_token text, admin_token_secret text);")
        db.sql("create table request_tokens(user_id integer, token text, token_secret text)");
        db.commit()


    def on_user_web_access(self, user_id, get_array, post_array):
        TWITTER_KEY = "1"
        db = a.get_db()

        if 'connect' in get_array and get_array['connect'] == 'twitter':
            consumer = oauth.Consumer(consumer_key, consumer_secret)
            client = oauth.Client(consumer)

            resp, content = client.request(request_token_url, "GET")
            if resp['status'] != '200':
                raise Exception("Invalid response %s." % resp['status'])

            request_token = dict(parse.parse_qsl(content.decode()))

            db.sql("INSERT INTO request_tokens(user_id, token, token_secret) VALUES(%s, '"+request_token['oauth_token']+"', '"+request_token['oauth_token_secret']+"')", (str(user_id),))
            db.commit()


            a.p('<p>Connexion a Twitter requise.</p>')
            a.p('<a href="'+authorize_url+'?oauth_token='+(request_token['oauth_token'])+'">Continuer sur Twitter</a>')

        elif 'twitter' in get_array and get_array["twitter"] == TWITTER_KEY:
            consumer = oauth.Consumer(consumer_key, consumer_secret)
            client = oauth.Client(consumer)

            oauth_token = get_array['oauth_token']
            oauth_verifier = get_array['oauth_verifier']

            request_token = db.sql('SELECT * FROM request_tokens WHERE user_id=%s', (str(user_id),))[0]

            token = oauth.Token(request_token[1],
                request_token[2])
            token.set_verifier(oauth_verifier)
            client = oauth.Client(consumer, token)

            resp, content = client.request(access_token_url, "POST")

            if resp['status'] != '200':
                raise Exception("Invalid response %s." % resp['status'])

            access_token = dict(parse.parse_qsl(content.decode()))

            db.sql("INSERT INTO usr(usr_id, usr_token, usr_token_secret) VALUES(%s, '"+access_token['oauth_token']+"', '"+access_token['oauth_token_secret']+"')", (str(user_id),))
            db.sql('DELETE FROM request_tokens WHERE user_id = %s', (str(user_id),))
            db.commit()

            a.p('<p>Twitter pairing successful</p>')
        else:

            a.p('<a href="'+a.get_url()+'&connect=twitter">Connect with Twitter</a>')

    def on_admin_web_access(self, user_id, get_array, post_array):
        pass

    def on_public_web_access(self, user_id, get_array, post_array):
        a.p("""
            <p>Link your Twitter account to Bobcat and tweet with SMS messages !</p>
            <h4>Commands</h4>
            
            <p><span class="label label-primary">twitter</span> <span class="label label-info">message</span> : tweet a message.</p>
            <p><span class="label label-primary">twittlt</span> <span class="label label-info">@user_name</span> : get the last tweet.</p>
            <p class="alert alert-info"><strong>Pssst!</strong> If you don't have an account, you can tweet on @ProxyBc with the <span class="label label-primary">twittbc</span> <span class="label label-info">message</span> command. Try it out ! </p>
            """)

        
        

a.init(TwitterBobcat(), 21)

