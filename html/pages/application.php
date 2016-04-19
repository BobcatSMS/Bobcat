<div class="container">
	<h2 class="page-header">
		Applications
	</h2>
	<div class="col-sm-3">
		<nav class="navbar"> 
			<ul class="nav nav-pills nav-stacked">
				<?php
				$req = $pdo->query("select * from applications where flea_id <> 15 order by name");

				while($d = $req->fetch()){
					echo '
					<li '. (isset($_GET['s']) && $d['flea_id'] == h($_GET['s']) ? 'class = "active"' : '') .' >
						<a href="?page=application&s=',$d['flea_id'], '">
							<p class="appname">', $d['name'], '</p>
							<p class="appdesc">', $d['description'], '</p>
						</a>
					</li>';
				}
				if(isset($_SESSION['role']) && $_SESSION['role'] == 'admin'){
					echo '<li><a href="?page=newapplication"><span class="appname">Nouvelle application</span></a></li>';
				}
				?>
			</ul>
		</nav>
	</div>


	<div class="col-sm-9">
		<?php
		$msg = '';

		if(isset($_GET['s'])){
			$req = $pdo->prepare('SELECT * FROM applications WHERE flea_id = ?');
			$req->execute([h($_GET['s'])]);
			$d = $req->fetch();

			$get = [];
			foreach($_GET as $k=>$g){
				if($k != 'page' && $k != 's')
					$get[$k] = $g;
			}
			$get = "'".json_encode($get)."'";
			$get = $get == "'[]'" ? "'{}'" : $get;
			$post = "'".json_encode($_POST)."'";
			$post = $post == "'[]'" ? "'{}'" : $post;

				//WELLS VERSION
				// if($d){

				// 	if((isset($_SESSION['id']) && $_SESSION['id'] == $d['admin']) || (isset($_SESSION['role']) && $_SESSION['role'] == 'admin')){
				// 		echo '<h2 class="page-header">Administration</h2><div class="well">', access_application($d['flea_id'], $_SESSION['id'], $get, $post, 'admin'), '</div>';
				// 	}
				// 	if(isset($_SESSION['role']) && $_SESSION['role'] == 'user'){
				// 		echo '<h2 class="page-header">Configuration</h2><div class="well">', access_application($d['flea_id'], $_SESSION['id'], $get, $post, 'user'), '</div>';
				// 	}
				// 	echo '<h2 class="page-header">Description</h2><div class="well">', access_application($d['flea_id'], 0, $get, $post, 'public'),'</div>';

				// }else{
				// 	$msg = '<div class="well"><p class="well well-lg">Application not found</p></div>';
				// }


				//PANELS VERSION

			if($d){

				if((isset($_SESSION['id']) && $_SESSION['id'] == $d['admin']) || (isset($_SESSION['role']) && $_SESSION['role'] == 'admin')){
					echo '<div class="panel panel-default"><div class="panel-heading">Administration</div><div class="panel-body">', access_application($d['flea_id'], $_SESSION['id'], $get, $post, 'admin'), '</div></div>';
				}
				if(isset($_SESSION['role']) && $_SESSION['role'] == 'user'){
					echo '<div class="panel panel-default"><div class="panel-heading">Configuration</div><div class="panel-body">', access_application($d['flea_id'], $_SESSION['id'], $get, $post, 'user'), '</div></div>';
				}
				echo '<div class="panel panel-default"><div class="panel-heading">Description</div><div class="panel-body">', access_application($d['flea_id'], 0, $get, $post, 'public'),'</div></div>';

			}else{
				$msg = '<p class="well well-lg">Application not found</p>';
			}
		}

		echo $msg;	
		?>
	</div>
</div>