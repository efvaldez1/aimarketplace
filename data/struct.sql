create table users(
	id SERIAL PRIMARY KEY,
	name text,
	email text,
	username text
);

CREATE TABLE category(
	id SERIAL PRIMARY KEY,
	added_on timestamp DEFAULT NOW(),
	name text
);


CREATE TABLE product(
	id SERIAL PRIMARY KEY,
	name text,
	description text,
	author_id integer REFERENCES users(id),
	added_on timestamp DEFAULT NOW(),
	category_id integer REFERENCES category(id)
);


CREATE TABLE offer(
	id SERIAL PRIMARY KEY,
	amount integer,
	offerdescription text,
	added_on timestamp DEFAULT NOW(),
	product_id integer REFERENCES product(id),
	user_id integer REFERENCES users(id)	
);


## how to connect all bidders in offer

#kill all psql connections
#sudo /etc/init.d/postgresql restart