<?php

function h($str){
	return trim(htmlspecialchars($str));
}

function access_application($application_id, $user_id,  $get, $post, $role='public'){
	global $pdo;
	// $req = $pdo->prepare("SELECT * FROM applications INNER JOIN languages ON applications.language_id = language.id WHERE flea_id = ?");
	// $req->execute([$application_id]);
	// $d = $req->fetch();

	if($role == 'admin')
		$access = 'on_admin_web_access';
	else if ($role == 'user')
		$access = 'on_user_web_access';
	else
		$access = 'on_public_web_access';


	exec('python3 '.'../src/applications/'.$application_id.'/main.py '.$access.' '.$user_id.' '.$get.' '.$post, $output);
	return implode("\n", $output);
}
