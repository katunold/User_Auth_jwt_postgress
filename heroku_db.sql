DROP DATABASE IF EXISTS "user_api_db";

CREATE DATABASE "user_api_db";

\connect "postgres://imxhfeqifoestz:689239e3f43d0bd11484b9dcc049e7ba3beed97f1f192dc49b5df388f43af2cd@ec2-54-225-97-112.compute-1.amazonaws.com:5432/d80tbmd64eh4km"

DROP SCHEMA IF EXISTS production CASCADE;

CREATE SCHEMA production;

CREATE TABLE production.user (
    user_id SERIAL NOT NULL PRIMARY KEY,
    user_name character varying(45) NOT NULL,
    email character varying(45) NOT NULL,
    registered_on timestamp(6) without time zone NOT NULL,
    password character varying(255) NOT NULL
);

CREATE TABLE production.blacklist_token (
    token_id SERIAL NOT NULL,
    token character varying(500) NOT NULL,
    blacklisted_on timestamp(6) without time zone
);

DROP SCHEMA IF EXISTS tests CASCADE;

CREATE SCHEMA tests;

CREATE TABLE tests.user (
    user_id SERIAL NOT NULL PRIMARY KEY,
    user_name character varying(45) NOT NULL,
    email character varying(45) NOT NULL,
    registered_on timestamp(6) without time zone NOT NULL,
    password character varying(255) NOT NULL
);

CREATE TABLE tests.blacklist_token (
    token_id SERIAL NOT NULL,
    token character varying(500) NOT NULL,
    blacklisted_on timestamp(6) without time zone NOT NULL
);