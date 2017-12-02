create table users(
	id SERIAL PRIMARY KEY,
	name text,
	email text,
	username text
);

CREATE TABLE category(
	id SERIAL PRIMARY KEY,
	name text
);


CREATE TABLE product(
	id SERIAL PRIMARY KEY,
	name text,
	description text,
	author integer REFERENCES users(id),
	added_on timestamp DEFAULT NOW(),
	category_id integer REFERENCES category(id)
);


CREATE TABLE offer(
	id SERIAL PRIMARY KEY,
	amount integer,
	offerdescription text,
	product_id integer REFERENCES product(id),
	user_id integer REFERENCES users(id)	
);

#kill all psql connections
#sudo /etc/init.d/postgresql restart