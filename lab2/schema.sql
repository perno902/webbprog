drop table if exists users;
create table users(
  email text primary key,
  password text,
  firstname text,
  familyname text,
  gender text,
  city text,
  country text
  );