<?php
	$msg = '';
	if(!isset($_SESSION['role']) || $_SESSION['role'] != 'admin')
		header('Location:?');

	if(isset($_POST['name']) && h($_POST['name']) != ''){
		if($pdo->exec("INSERT INTO fleas (type) VALUES ('app')") === false)
			die(print_r($pdo->errorInfo()));

		$ok = True;

		if(!($id = $pdo->lastInsertId('fleas_id_seq')))
			die(print_r($pdo->errorInfo()));
		echo 'id=',$id;


		if(h($_POST['slug']) == ""){
			$slug = $id;
		}else{
			$slug = $_POST['slug'];
		}

		$req = $pdo->prepare("SELECT COUNT(*) as nb FROM applications WHERE slug = ?");
		if( $req->execute([$slug]) === false)
			die(print_r($pdo->errorInfo()));
		if($req->fetch()['nb'] > 0){
			$msg .= '<p>Slug already exists</p>';
			$ok = False;
		}


		$req = $pdo->prepare("INSERT INTO 
			applications(flea_id, name, description, slug, server_id, language_id, admin)
			VALUES (:flea_id, :name, :description, :slug, :server_id, :language_id, :admin)");

		if(!$req->execute(["flea_id"=>$id, "name"=>h($_POST['name']), "description"=>h($_POST['description']), "slug"=>h($_POST['slug']), "server_id"=>0, "language_id"=>h($_POST['language']), "admin"=>h($_POST['admin'])]))
			die(print_r($pdo->errorInfo()));

		foreach(explode(" ", $_POST['commands']) as $command){
			echo $command;
		}


		if(!mkdir('/home/pi/bobcat/src/applications/'.$id))
			die("Can't create dir ".'/home/pi/bobcat/src/applications/'.$id);
		

		if(!$pdo->query("CREATE USER bobcat_".$id." encrypted password 'bobcat_".$id."'"))
			die(print_r($pdo->errorInfo()));

		if(!$pdo->query("CREATE DATABASE bobcat_".$id." owner bobcat_".$id))
			die(print_r($pdo->errorInfo()));



		if($ok)
			$msg .= '<p>Application created</p>';

	}
	echo $msg;


$req_languages = $pdo->query("SELECT * FROM languages ORDER BY name");
$req_users = $pdo->query("SELECT * FROM users ORDER BY username");

?>

<form method="post" action="">
	<label for="name">Name</label>
	<input type="text" name="name" placeholder="name" />

	<label for="description">Description</label>
	<textarea name="description" placeholder="description"></textarea>


	<label for="slug">Slug</label>
	<input type="text" name="slug" placeholder="slug" />
	
	<label for="language">Language</label>
	<select name="language">
		<?php
			while($d = $req_languages->fetch()){
				echo '<option value="'.$d['id'].'">'.$d['name'].'</option>';
			}
		?>
	</select>

	<label for="admin">Admin</label>
	<select name="admin">
		<?php
			while($d = $req_users->fetch()){
				echo '<option '.($d['flea_id']==$_SESSION['id']?'selected="selected"':'').' value="'.$d['flea_id'].'">'.$d['username'].' - '.$d['phone_number'].'</option>';
			}
		?>
	</select>
	
	<label for="commands">Commands (one per line)</label>
	<textarea name="commands"></textarea>
	
	<input type="submit" value="send" />
</form>
