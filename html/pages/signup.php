<?php
    $msg = '';
    if(isset($_POST['password']) && isset($_POST['password_conf'])){
        if(!isset($_POST['login']) && !isset($_POST['mail']) && isset($_POST['phone_number'])){
            $msg .= "<p>You have to key in a login, mail or phone number.</p>";
        }else{
            $ok = 1;
            
            if(h($_POST['password']) != h($_POST['password_conf'])){
                $ok = 0;
                $msg .= '<p>Passwords don\'t match.';
            }
            
            $req = $pdo->prepare('SELECT count(*) as nb FROM users WHERE username = ?');
            $req->execute([h($_POST['login'])]);
            $d = $req->fetch();
            if($d['nb']>0 && h($_POST['login'])){
                $msg .= '<p>Username already registred.</p>';
                $ok = 0;
            }
            
            $req = $pdo->prepare('SELECT count(*) as nb FROM users WHERE phone_number = ?');
            $req->execute([h($_POST['phone_number'])]);
            $d = $req->fetch();
            if($d['nb']>0 && h($_POST['phone_number'])){
                $msg .= '<p>Phone number already registred.</p>';
                $ok = 0;
            }

            $req = $pdo->prepare('SELECT count(*) as nb FROM users WHERE mail = ?');
            $req->execute([h($_POST['mail'])]);
            $d = $req->fetch();
            if($d['nb']>0 && h($_POST['mail'])){
                $msg .= '<p>Mail address already registred.</p>';
                $ok = 0;
            }

            if($ok){

                $req = $pdo->prepare('SELECT * FROM addUser(?, ?, ?, ?)');
                $req->execute([
                    h($_POST['phone_number']),
                    h($_POST['login']),
                    md5($_POST['password']),
                    h($_POST['mail'])
                ]);
                
                $_SESSION['login'] = h($_POST['login']);
                $_SESSION['id'] = $id;
                $_SESSION['role'] = "user";

                $msg .= '<p>You registered successfully.</p>';
                header('Location:?page=application');
            }
        }
        
    }

    $vars = [];
    foreach (['login', 'mail', 'phone_number'] as $key) {
        if(isset($_POST[$key]))
            $vars[$key] = h($_POST[$key]);
        else
            $vars[$keys] = '';
    }
?>

<div class="container">
    <div class="page_header">
        <h1>Sign Up</h1>
    </div>  
    <form role="form" class="form-horizontal" method="POST", action="">
        
        <div class="form-group">
            <label class="control-label col-sm-2" for="login">Username :</label>
            <div class="col-sm-4">
                <input class="form-control" type="text" placeholder="Username" name="login" value="<?php echo $vars['login']; ?>" />
            </div>
        </div>

        <div class="form-group">
            <label class="control-label col-sm-2" for="mail">Email :</label>
            <div class="col-sm-4">
                <input class="form-control" type="text" placeholder="flea@bob.cat" name="mail" value="<?php echo $vars['mail']; ?>" />
            </div>
        </div>

        <div class="form-group">
            <label class="control-label col-sm-2" for="phone_number">Phone number :</label>
            <div class="col-sm-4">
                <input
                    class="form-control"
                    type="text"
                    placeholder="+336********"
                    name="phone_number"
                    value="<?php echo $vars['phone_number']; ?>"
                    pattern="\+33[67][0-9]{8}"
                    title="Numéro de téléphone mobile français (+336******** ou +337********)"
                />
            </div>
        </div>

        <div class="form-group">
            <label class="control-label col-sm-2" for="password">Password :</label>
            <div class="col-sm-4">
                <input class="form-control" type="password" placeholder="Not 1234 please." name="password" />
            </div>
        </div>

        <div class="form-group">
            <label class="control-label col-sm-2" for="password_conf">Confirm password :</label>
            <div class="col-sm-4">
                <input class="form-control" type="password" placeholder="Not 1234 please." name="password_conf" />
            </div>
        </div>
        
        <div class="form-group">
            <div class="col-sm-offset-2 col-sm-4">
                <button type="submit" class="btn btn-default">Submit</button>
            </div>
        </div>
    </form>
    <div class="col-sm-6">
        <?php echo $msg; ?>
    </div>
</div>
