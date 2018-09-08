DROP DATABASE IF EXISTS "user_api_db";

CREATE DATABASE "user_api_db";

\connect "user_api_db"

DROP SCHEMA IF EXISTS production CASCADE;

CREATE SCHEMA production;

CREATE TABLE production.user (
    user_id integer NOT NULL,
    user_name character varying(45) NOT NULL,
    email character varying(45) NOT NULL,
    registered_on timestamp(6) without time zone NOT NULL,
    password character varying(255) NOT NULL
);

DROP SCHEMA IF EXISTS tests CASCADE;

CREATE SCHEMA tests;

CREATE TABLE tests.user (
    user_id integer NOT NULL,
    user_name character varying(45) NOT NULL,
    email character varying(45) NOT NULL,
    registered_on timestamp(6) without time zone NOT NULL,
    password character varying(255) NOT NULL
);
