-- Conventions (check cakephp ones)
-- variable_name or column_name
-- table_name
-- functionName
-- vars
-- in_name : param
-- out_name : param as return
-- ret_name : var that will be returned
-- var_name : var


CREATE TABLE if not exists fleas(
	id SERIAL PRIMARY KEY,
	type text
);

CREATE TABLE if not exists users(
	flea_id integer PRIMARY KEY,
	username text,
	password text,
	mail text,
	phone_number text,
	role text,
	FOREIGN KEY (flea_id) REFERENCES fleas(id)
);

CREATE TABLE if not exists servers(
	flea_id integer PRIMARY KEY,
	pubkey text,
	ip_adress text,
	uniq_ident integer,
	FOREIGN KEY (flea_id) REFERENCES fleas(id)
);

CREATE TABLE if not exists commands(
	application_id integer,
	value text,
	UNIQUE(value),
	FOREIGN KEY (application_id) REFERENCES fleas(id)
);

CREATE TABLE if not exists applications(
	flea_id integer PRIMARY KEY,
	name text,
	description text,
	slug text,
	server_id integer,
	language_id integer,
	UNIQUE(slug),
	FOREIGN KEY (flea_id) REFERENCES fleas(id)
);

CREATE TABLE if not exists roles(
	id SERIAL PRIMARY KEY,
	name text,
	UNIQUE(name)
);

CREATE TABLE if not exists applications_users(
	first_id integer,
	second_id integer,
	uniqueid integer NOT NULL,
	role integer, -- Les privilèges qu'a l'utilisateur sur l'application
	UNIQUE(uniqueid),
	UNIQUE(first_id, second_id),
	FOREIGN KEY (role) REFERENCES roles(id),
	--CHECK (first_id <= second_id)
);




CREATE TABLE if not exists languages(
	id SERIAL PRIMARY KEY,
	name text,
	command text --the command that take the program as paramater 'python3' for instance
);



CREATE OR REPLACE FUNCTION applicationIdFromCommand (command text) RETURNS integer AS $$
BEGIN
	RETURN (SELECT application_id FROM Commands WHERE value = command);
END; $$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION uniqueidFromTwoFleas (in_id1 integer, in_id2 integer) RETURNS integer
AS $$
DECLARE
	ret_id integer;
	var_tmp integer;
BEGIN

	-- The applications_users table got the ids in asc order
	IF in_id1 > in_id2 THEN
		var_tmp := in_id1;
		in_id1 := in_id2;
		in_id2 := var_tmp;
	END IF;


	SELECT uniqueid into ret_id
		FROM applications_users 
		WHERE var = applicationid AND user_id = userid;

	IF ret_id IS NULL THEN
		SELECT (ROUND(random * 100000000)) into ret_id FROM random();


		INSERT INTO applications_users(first_id, second_id, uniqueid, role)
			VALUES(in_id1, in_id2, ret_id, getRoleId('default'));

	END IF;

	RETURN ret_id;
END; $$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION addFlea (in_type text) RETURNS integer
AS $$
DECLARE
	ret_id integer;
BEGIN
	
	-- BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
		INSERT INTO fleas(type) VALUES(in_type);
		SELECT currval(pg_get_serial_sequence('fleas','id')) into ret_id;
	-- END TRANSACTION;

	RETURN ret_id;
END; $$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION userPhoneNumbreFromId(in_id int)
RETURNS text AS $$
BEGIN
	RETURN (SELECT phone_number FROM users WHERE flea_id = in_id);
END; $$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION fleaTypeFromId(in_id int)
RETURNS text AS $$
BEGIN
	RETURN (SELECT type FROM fleas WHERE id = in_id);
END; $$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION existsFlea(in_id int)
RETURNS boolean AS $$
BEGIN
	RETURN ((SELECT COUNT(*) FROM fleas WHERE id = in_id) = 1);
END; $$ LANGUAGE plpgsql;


-- TODO add a table contening admin ids in parameter
CREATE OR REPLACE FUNCTION addApplication (in_name text, in_description text, in_slug text, in_language_id integer, in_server_id integer DEFAULT 0) RETURNS integer
AS $$
DECLARE
	ret_flea_id integer;
BEGIN
	ret_flea_id = add_flea('app');

	INSERT INTO applications(flea_id, name, description, slug, server_id, language_id, admin) 
		VALUES(ret_flea_id, in_name, in_description, in_slug, in_server_id, in_language_id, in_admin);

	EXECUTE format('CREATE USER application_%I ENCRYPTED PASSWORD ''%I'' ', in_name, in_name);
	EXECUTE format('CREATE DATABASE application_%I OWNER application_%I', in_name, in_name);

	RETURN ret_flea_id;
END; $$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION addUser (in_phone text, in_username text DEFAULT '', in_password text DEFAULT '', in_mail text DEFAULT '') RETURNS integer
AS $$
DECLARE
	ret_flea_id integer;
BEGIN
	IF ( SELECT phone_number FROM users WHERE phone_number = in_phone) IS NOT NULL THEN
		UPDATE users SET username = in_username WHERE phone_number = in_phone;
		UPDATE users SET mail = in_mail WHERE phone_number = in_phone;
		UPDATE users SET password = in_password WHERE phone_number = in_phone;
		
	ELSE
		ret_flea_id = add_flea('user');
		INSERT INTO users(flea_id, username, password, mail, phone_number) 
		VALUES(ret_flea_id, in_username, in_password, in_mail, in_phone_number);
	END IF;

	RETURN ret_flea_id;
END; $$ LANGUAGE plpgsql;	

--use PERFORM to call it
CREATE OR REPLACE FUNCTION addCommands(in_application_id integer, in_value text) RETURNS void
AS $$
BEGIN
	IF (SELECT * FROM commands WHERE value = in_value) IS NULL THEN
		INSERT INTO commands(application_id, value) VALUES(in_application_id, in_value);
	ELSE
		RAISE EXCEPTION 'Command already exists : %', in_value;
	END IF;

END; $$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION getRoleId(in_name text) RETURNS integer
AS $$
DECLARE
	ret_id integer;
BEGIN
	SELECT name into ret_id FROM roles WHERE name = in_name;

	IF ret_id IS NULL THEN
		RAISE EXCEPTION 'Role not found : %', in_name;
	END IF;

	RETURN ret_id;

END; $$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION getRoleName(in_id integer) RETURNS text
AS $$
DECLARE
	ret_name text;
BEGIN
	SELECT name into ret_name FROM roles WHERE id = in_id;

	IF ret_name IS NULL THEN
		RAISE EXCEPTION 'Role not found : %', in_id;
	END IF;

	RETURN ret_name;

END; $$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION setRole(in_id1 integer, in_id2 integer, in_role integer) RETURNS void
AS $$
DECLARE
	var_uniqueid integer;
BEGIN
	SELECT ret_id into var_uniqueid FROM uniqueidFromTwoFleas(in_id1, in_id2);
	UPDATE applications_users SET role = in_role WHERE uniqueid = var_unique;

END; $$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION test() RETURNS boolean
AS $$
DECLARE
	var_user_adrian integer;
	var_user_axce integer;
	var_user_jules integer;
	var_app_dice integer;
BEGIN

	INSERT INTO languages(name, command) VALUES('Python', 'python3.5');
	INSERT INTO roles(name) VALUES('default');
	INSERT INTO roles(name) VALUES('user');
	INSERT INTO roles(name) VALUES('admin');
	SELECT ret_id into var_user_adrian FROM addUser('', 'adrian', 'Admin', '');
	SELECT ret_id into var_user_axce FROM addUser('', 'axce', 'Admin', '');
	SELECT ret_id into var_user_jules FROM addUser('', 'jules', 'Admin', '');
	SELECT ret_id into var_app_dice FROM addApplication('dice', 'Dice roll', 'dice', 1);
	PERFORM addCommands(var_app_dice, 'dice');
	PERFORM setRole(var_app_dice, var_user_jules, 'admin');


END; $$ LANGUAGE plpgsql;




