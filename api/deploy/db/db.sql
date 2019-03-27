create database mapitout;
create role mapitout with password 'insecure';
grant all privileges on database mapitout to mapitout;
grant connect on database mapitout to mapitout;
alter role mapitout superuser;
alter role mapitout with login;

