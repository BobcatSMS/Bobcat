<?php
    $msg = '';
    if(isset($_POST['login_co']) && isset($_POST['password_co'])){
        $req = $pdo->prepare('SELECT * FROM users WHERE password = ? AND (username = ? OR  mail = ? OR  phone_number = ?)');
        $req->execute([md5($_POST['password_co']), h($_POST['login_co']), h($_POST['login_co']), h($_POST['login_co'])]);
        
        if($d = $req->fetch()){
            $_SESSION['login'] = $d['username'];
            $_SESSION['id'] = $d['flea_id'];
            $_SESSION['role'] = $d['role'];
            $msg .= '<p class="alert alert-success">Login successful</p>';
            header('Location:?page=application');
        }else{
            $msg .= '<p class="alert alert-danger">Login failed</p>';
        }

    }
?>

<div class="container">
    <div class="page_header">
        <h1>Login</h1>
    </div>  
    <form role="form" class="form-horizontal" method="POST" action="">
        <div class="form-group">
            <label class="control-label col-sm-2" for="login_co">Login :</label>
            <div class="col-sm-4">
                <input class="form-control" type="text" placeholder="Username / phone / mail" name="login_co" />
            </div>
        </div>

        <div class="form-group">
            <label class="control-label col-sm-2" for="password_co">Password :</label>
            <div class="col-sm-4">
                <input class="form-control" type="password" placeholder="Password" name="password_co" />
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



