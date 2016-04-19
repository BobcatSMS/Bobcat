<?php

	if(isset($_POST['name']) && isset($_POST['message'])){
		mail('admin@bcat.fr', 'bcat.fr message from - '.h($_POST['name']), h($_POST['message']));
	}

?>

<div class="container">
    <h1 class="page_header">Contact</h1>

    <form role="form" class="form-horizontal" method="POST" action="">
            <div class="form-group">
                <label class="control-label col-sm-2" for="name">Name :</label>
                <div class="col-sm-4">
                    <input class="form-control" type="text" placeholder="Name" name="name" />
                </div>
            </div>

            <div class="form-group">
                <label class="control-label col-sm-2" for="message">Message :</label>
                <div class="col-sm-4">
                  	<textarea class="form-control" rows="5" name="message" placeholder="Enter your message here"></textarea>
                </div>
            </div>

        <div class="form-group">
            <div class="col-sm-offset-2 col-sm-4">
                <button type="submit" class="btn btn-default">Submit</button>
            </div>
        </div>
    </form>
</div>
