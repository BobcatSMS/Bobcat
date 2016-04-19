CREATE TABLE if not exists fleas(
	id integer PRIMARY KEY,
	type varchar(10)
);

CREATE TABLE if not exists users(
	flea_id integer PRIMARY KEY,
	username varchar(30),
	password varchar(30),
	mail varchar(30),
	phone_number varchar(30),
	role varchar(10),
	FOREIGN KEY (flea_id) REFERENCES fleas(id)
);

CREATE TABLE if not exists servers(
	flea_id integer PRIMARY KEY,
	pubkey text,
	ip_adress varchar(20),
	uniq_ident integer,
	FOREIGN KEY (flea_id) REFERENCES fleas(id)
);

CREATE TABLE if not exists commands(
	application_id integer PRIMARY KEY,
	value varchar(20),
	parameter varchar(20) NOT NULL DEFAULT message, --the parameter passed to the app when the command is called
	FOREIGN KEY (application_id) REFERENCES fleas(id)
);

CREATE TABLE if not exists applications(
	flea_id integer PRIMARY KEY,
	name varchar(30),
	description text,
	slug varchar(20),
	server_id integer,
	language_id integer,
	admin integer,
	UNIQUE(slug),
	FOREIGN KEY (admin) REFERENCES users(flea_id),
	FOREIGN KEY (flea_id) REFERENCES fleas(id)
);


CREATE TABLE if not exists applications_users(
	user_id integer,
	application_id integer,
	uniqueid integer NOT NULL,
	UNIQUE(uniqueid)
);



CREATE TABLE if not exists languages(
	id integer PRIMARY KEY,
	name varchar(30),
	command text --the command that take the program as paramater 'python3' for instance
);

INSERT INTO languages(name, command) VALUES("Python", "python3.5");
