PGDMP     3                    y            casting_agency    13.1    13.1     ?           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            ?           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            ?           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            ?           1262    24693    casting_agency    DATABASE     n   CREATE DATABASE casting_agency WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Hungarian_Hungary.1250';
    DROP DATABASE casting_agency;
                postgres    false            ?            1259    24704    actor    TABLE     ?   CREATE TABLE public.actor (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    age integer NOT NULL,
    gender character varying NOT NULL
);
    DROP TABLE public.actor;
       public         heap    postgres    false            ?            1259    24702    actor_id_seq    SEQUENCE     ?   CREATE SEQUENCE public.actor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.actor_id_seq;
       public          postgres    false    203            ?           0    0    actor_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.actor_id_seq OWNED BY public.actor.id;
          public          postgres    false    202            ?            1259    24713    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap    postgres    false            ?            1259    24696    movie    TABLE     ?   CREATE TABLE public.movie (
    id integer NOT NULL,
    title character varying(150) NOT NULL,
    release_date character varying(10) NOT NULL
);
    DROP TABLE public.movie;
       public         heap    postgres    false            ?            1259    24694    movie_id_seq    SEQUENCE     ?   CREATE SEQUENCE public.movie_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.movie_id_seq;
       public          postgres    false    201            ?           0    0    movie_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.movie_id_seq OWNED BY public.movie.id;
          public          postgres    false    200            .           2604    24707    actor id    DEFAULT     d   ALTER TABLE ONLY public.actor ALTER COLUMN id SET DEFAULT nextval('public.actor_id_seq'::regclass);
 7   ALTER TABLE public.actor ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    203    202    203            -           2604    24699    movie id    DEFAULT     d   ALTER TABLE ONLY public.movie ALTER COLUMN id SET DEFAULT nextval('public.movie_id_seq'::regclass);
 7   ALTER TABLE public.movie ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    200    201    201            ?          0    24704    actor 
   TABLE DATA           6   COPY public.actor (id, name, age, gender) FROM stdin;
    public          postgres    false    203   ?       ?          0    24713    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public          postgres    false    204   3       ?          0    24696    movie 
   TABLE DATA           8   COPY public.movie (id, title, release_date) FROM stdin;
    public          postgres    false    201   P       ?           0    0    actor_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.actor_id_seq', 4, true);
          public          postgres    false    202            ?           0    0    movie_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.movie_id_seq', 4, true);
          public          postgres    false    200            2           2606    24712    actor actor_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.actor
    ADD CONSTRAINT actor_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.actor DROP CONSTRAINT actor_pkey;
       public            postgres    false    203            4           2606    24717 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public            postgres    false    204            0           2606    24701    movie movie_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.movie
    ADD CONSTRAINT movie_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.movie DROP CONSTRAINT movie_pkey;
       public            postgres    false    201            ?   t   x?3?NN,?I-)Q???H?+.???46?LK?M?I?2??OJ-*Qp?/?K?T?*??45??s??dV%&??d(???????p:?楦d&?(8??MHJ,I??41?h????? ??&3      ?      x?????? ? ?      ?   y   x?3?t?O.?/R.)J?KO?4204?54?50?2??,??S?M??X???qs??&?d&?+??)?d?*?'?$VT??????r?p:???+*?Rp?KIO??l	4V?Ȍ+F??? %? ?     