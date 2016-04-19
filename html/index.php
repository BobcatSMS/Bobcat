<?php
	$pdo = new PDO('pgsql:host=localhost;dbname=bobcat;user=bobcat;password=bobcat');
	$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	require 'functions/functions.php';
	session_start();
	$PRIVATE_PAGES = ['logout','newapplication'];
	$PUBLIC_PAGES = ["about", "contact", 'application', "login", "signup"];
	$DEFAULT_PAGE = "home";
	$DEBUG = false;

	if($DEBUG){
		print_r($_SESSION);
		print_r($_POST);
	}

	if(isset($_GET['page'])){
		$page = h($_GET['page']);
	}else{
		$page = 'home';
	}
	

?>

<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css" />
	<link rel="stylesheet" type="text/css" href="css/style.css" />
	
	<meta name="viewport" content="width=device-width, initial-scale=1" />
	<meta charset="UTF-8" />
	
	<script type="text/javascript" src="js/jquery-1.12.3.min.js"></script>
	<script type="text/javascript" src="js/bootstrap.min.js"></script>
	
	<title>Bobcat !</title>
</head>
	<body>
		<nav class="navbar navbar-default navbar-static-top"> 
			<div class="container-fluid">
				<div class="navbar-header">
					<button type = "button" class = "navbar-toggle" data-toggle = "collapse" data-target = "#navbar-collapse">
						<span class = "sr-only">Toggle navigation</span>
						<span class = "icon-bar"></span>
						<span class = "icon-bar"></span>
						<span class = "icon-bar"></span>
					</button>
				    <a class="navbar-brand" href="?">Bobcat</a>
			    </div>
			    <div class = "collapse navbar-collapse" id = "navbar-collapse">
					<ul class="nav navbar-nav">
						<li <?php echo $page == 'home'?'class="active"' : '' ?>><a href="?">Home</a></li>
						<li <?php echo $page =="about"?'class="active"' : '' ?>><a href="?page=about">About</a></li>
						<li <?php echo $page =="contact"?'class="active"' : '' ?>><a href="?page=contact">Contact us !</a></li>
						<li><a href="https://github.com/bobcatsms/bobcat">Source on GitHub</a></li>
					</ul>
					<ul class="nav navbar-nav navbar-right">
						<li <?php echo $page =="application"?'class="active"' : '' ?>><a href="?page=application"><span class="glyphicon glyphicon-cog"></span> Applications</a></li>
						<?php if (!isset($_SESSION['login'])){ ?>
							<li <?php echo $page =="signup"?'class="active"' : '' ?>><a href="?page=signup"><span class="glyphicon glyphicon-user"></span> Sign Up</a></li>
							<li <?php echo $page =="login"?'class="active"' : '' ?>><a href="?page=login"><span class="glyphicon glyphicon-log-in"></span> Login</a></li>
						<?php }else{ ?>
							
							<li <?php echo $page =="logout"?'class="active"' : '' ?>><a href="?page=logout"><span class="glyphicon glyphicon-log-out"></span> Logout</a></li>
						<?php } ?>
					</ul>
				</div>
			</div>
		</nav>
		<?php
			if(isset($_GET['page'])){

				if(in_array(h($_GET['page']), $PUBLIC_PAGES)){
					include 'pages/'.h($_GET['page']).'.php';

				}else if(!isset($_SESSION['login'])){
					header('Location:?');
					exit();
				}else if(in_array(h($_GET['page']), $PRIVATE_PAGES)){
					include 'pages/'.h($_GET['page']).'.php';
				}else{
					include 'pages/'.$DEFAULT_PAGE.'.php';
				}
			}else{
				include 'pages/'.$DEFAULT_PAGE.'.php';
			}
		?>
	</body>
</html>
