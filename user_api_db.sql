PGDMP         	                v            user_api_db    10.4    10.4     *           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            +           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            ,           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false            -           1262    29036    user_api_db    DATABASE     }   CREATE DATABASE user_api_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';
    DROP DATABASE user_api_db;
             postgres    false                        2615    29038 
   production    SCHEMA        CREATE SCHEMA production;
    DROP SCHEMA production;
             postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false            .           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    3                        2615    29037    tests    SCHEMA        CREATE SCHEMA tests;
    DROP SCHEMA tests;
             postgres    false                        3079    12964    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false            /           0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    1            �            1259    29081    user    TABLE       CREATE TABLE production."user" (
    user_id integer NOT NULL,
    user_name character varying(45) NOT NULL,
    email character varying(45) NOT NULL,
    registered_on timestamp(6) without time zone NOT NULL,
    password character varying(255) NOT NULL
);
    DROP TABLE production."user";
    
   production         postgres    false    5            �            1259    29079    user_user_id_seq    SEQUENCE     �   CREATE SEQUENCE production.user_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE production.user_user_id_seq;
    
   production       postgres    false    201    5            0           0    0    user_user_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE production.user_user_id_seq OWNED BY production."user".user_id;
         
   production       postgres    false    200            �            1259    29069    user    TABLE     �   CREATE TABLE tests."user" (
    user_id integer NOT NULL,
    user_name character varying(45) NOT NULL,
    email character varying(45) NOT NULL,
    registered_on timestamp(6) without time zone NOT NULL,
    password character varying(255) NOT NULL
);
    DROP TABLE tests."user";
       tests         postgres    false    6            �            1259    29067    user_user_id_seq    SEQUENCE     �   CREATE SEQUENCE tests.user_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE tests.user_user_id_seq;
       tests       postgres    false    199    6            1           0    0    user_user_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE tests.user_user_id_seq OWNED BY tests."user".user_id;
            tests       postgres    false    198            �
           2604    29084    user user_id    DEFAULT     v   ALTER TABLE ONLY production."user" ALTER COLUMN user_id SET DEFAULT nextval('production.user_user_id_seq'::regclass);
 A   ALTER TABLE production."user" ALTER COLUMN user_id DROP DEFAULT;
    
   production       postgres    false    201    200    201            �
           2604    29072    user user_id    DEFAULT     l   ALTER TABLE ONLY tests."user" ALTER COLUMN user_id SET DEFAULT nextval('tests.user_user_id_seq'::regclass);
 <   ALTER TABLE tests."user" ALTER COLUMN user_id DROP DEFAULT;
       tests       postgres    false    199    198    199            '          0    29081    user 
   TABLE DATA               X   COPY production."user" (user_id, user_name, email, registered_on, password) FROM stdin;
 
   production       postgres    false    201   �       %          0    29069    user 
   TABLE DATA               S   COPY tests."user" (user_id, user_name, email, registered_on, password) FROM stdin;
    tests       postgres    false    199   �       2           0    0    user_user_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('production.user_user_id_seq', 15, true);
         
   production       postgres    false    200            3           0    0    user_user_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('tests.user_user_id_seq', 43, true);
            tests       postgres    false    198            �
           2606    29090    user user_email_key 
   CONSTRAINT     U   ALTER TABLE ONLY production."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);
 C   ALTER TABLE ONLY production."user" DROP CONSTRAINT user_email_key;
    
   production         postgres    false    201            �
           2606    29086    user user_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY production."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (user_id);
 >   ALTER TABLE ONLY production."user" DROP CONSTRAINT user_pkey;
    
   production         postgres    false    201            �
           2606    29088    user user_user_name_key 
   CONSTRAINT     ]   ALTER TABLE ONLY production."user"
    ADD CONSTRAINT user_user_name_key UNIQUE (user_name);
 G   ALTER TABLE ONLY production."user" DROP CONSTRAINT user_user_name_key;
    
   production         postgres    false    201            �
           2606    29078    user user_email_key 
   CONSTRAINT     P   ALTER TABLE ONLY tests."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);
 >   ALTER TABLE ONLY tests."user" DROP CONSTRAINT user_email_key;
       tests         postgres    false    199            �
           2606    29074    user user_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY tests."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (user_id);
 9   ALTER TABLE ONLY tests."user" DROP CONSTRAINT user_pkey;
       tests         postgres    false    199            �
           2606    29076    user user_user_name_key 
   CONSTRAINT     X   ALTER TABLE ONLY tests."user"
    ADD CONSTRAINT user_user_name_key UNIQUE (user_name);
 B   ALTER TABLE ONLY tests."user" DROP CONSTRAINT user_user_name_key;
       tests         postgres    false    199            '     x�uͻr�@@�z�)R؊���\��:�d^�����1�bD�>Iis�3��+%:��5�$Y���R��C��`��֨�I���*D�J�{$i;,���,��g�(6ݽ!����㇖��V_26k������s}����
0��?0��{^H�a7�)�~)S�4qH;��s�x��I�5�SEkLt4���<�L[e
���3�D�~��7��_��=m����v��ܵECH>ܱ���#��1�4�_�      %      x������ � �     