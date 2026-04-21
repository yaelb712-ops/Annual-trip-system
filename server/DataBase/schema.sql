CREATE DATABASE AnnualTripSystem

use AnnualTripSystem
go

create table Students(
id int identity (1,1) primary key,
firstName varchar(20) not null,
lastName varchar(20) not null,
identityNumber varchar(9) not null unique,
class varchar(10) not null
)

create table Teachers(
id int identity (1,1) primary key,
firstName varchar(20) not null,
lastName varchar(20) not null,
identityNumber varchar(9) not null unique,
class varchar(10) not null
)

create table Locations(
id int identity (1,1) primary key,
studentIdentity varchar(9) not null foreign key references Students(identityNumber),
longitude float not null,
latitude float not null,
timeS datetime not null
)