drop table if exists users;
drop table if exists loggedInUsers;

create table users(
  email text primary key,
  password text,
  firstname text,
  familyname text,
  gender text,
  city text,
  country text
  );

create table loggedInUsers (
  token text primary key,
  email text,
  foreign key(email) references users(email)
);