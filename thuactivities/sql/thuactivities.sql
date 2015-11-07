--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = true;

--
-- Name: activity; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE activity (
    id bigint NOT NULL,
    title character(50) NOT NULL,
    "time" timestamp(6) with time zone NOT NULL,
    description text,
    number_of_tickets integer NOT NULL,
    tickets_sold integer DEFAULT 0 NOT NULL,
    classroom_id bigint
);


--
-- Name: TABLE activity; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE activity IS 'information of activities';


--
-- Name: COLUMN activity.number_of_tickets; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN activity.number_of_tickets IS 'initial number of tickets';


--
-- Name: COLUMN activity.tickets_sold; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN activity.tickets_sold IS 'number of tickets sold';


--
-- Name: COLUMN activity.classroom_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN activity.classroom_id IS 'the classroom of the activity';


--
-- Name: activity_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE activity_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: activity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE activity_id_seq OWNED BY activity.id;


--
-- Name: classroom; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE classroom (
    id bigint NOT NULL,
    name character(50) NOT NULL
);


--
-- Name: TABLE classroom; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE classroom IS 'information of classrooms';


--
-- Name: classroom_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE classroom_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: classroom_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE classroom_id_seq OWNED BY classroom.id;


--
-- Name: schedule; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE schedule (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    activity_id bigint NOT NULL,
    seat_id bigint,
    ticket text NOT NULL,
    presence boolean
);


--
-- Name: COLUMN schedule.user_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN schedule.user_id IS 'student id';


--
-- Name: COLUMN schedule.activity_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN schedule.activity_id IS 'related activity';


--
-- Name: COLUMN schedule.seat_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN schedule.seat_id IS 'related seat';


--
-- Name: COLUMN schedule.ticket; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN schedule.ticket IS 'QR code';


--
-- Name: COLUMN schedule.presence; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN schedule.presence IS 'whether the student be present';


--
-- Name: schedule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE schedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: schedule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE schedule_id_seq OWNED BY schedule.id;


--
-- Name: seat; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE seat (
    id bigint NOT NULL,
    classroom_id bigint NOT NULL,
    name character(50) NOT NULL
);


--
-- Name: TABLE seat; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE seat IS 'information of seats';


--
-- Name: seat_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE seat_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: seat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE seat_id_seq OWNED BY seat.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE "user" (
    id bigint NOT NULL,
    name character(20) NOT NULL,
    gender boolean DEFAULT true NOT NULL,
    telephone character(20),
    wechat_id character(50) NOT NULL,
    verified boolean DEFAULT false NOT NULL,
    priority integer DEFAULT 10 NOT NULL
);


--
-- Name: TABLE "user"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE "user" IS 'information of users';


--
-- Name: COLUMN "user".id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN "user".id IS 'student id';


--
-- Name: COLUMN "user".name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN "user".name IS 'student name';


--
-- Name: COLUMN "user".gender; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN "user".gender IS 'gender';


--
-- Name: COLUMN "user".telephone; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN "user".telephone IS 'telephone number';


--
-- Name: COLUMN "user".wechat_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN "user".wechat_id IS 'wechat id';


--
-- Name: COLUMN "user".verified; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN "user".verified IS 'whether the account is verified';


--
-- Name: COLUMN "user".priority; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN "user".priority IS 'priority';


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY activity ALTER COLUMN id SET DEFAULT nextval('activity_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY classroom ALTER COLUMN id SET DEFAULT nextval('classroom_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY schedule ALTER COLUMN id SET DEFAULT nextval('schedule_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY seat ALTER COLUMN id SET DEFAULT nextval('seat_id_seq'::regclass);


--
-- Data for Name: activity; Type: TABLE DATA; Schema: public; Owner: -
--

COPY activity (id, title, "time", description, number_of_tickets, tickets_sold, classroom_id) FROM stdin;
\.


--
-- Name: activity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('activity_id_seq', 1, false);


--
-- Data for Name: classroom; Type: TABLE DATA; Schema: public; Owner: -
--

COPY classroom (id, name) FROM stdin;
\.


--
-- Name: classroom_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('classroom_id_seq', 1, false);


--
-- Data for Name: schedule; Type: TABLE DATA; Schema: public; Owner: -
--

COPY schedule (id, user_id, activity_id, seat_id, ticket, presence) FROM stdin;
\.


--
-- Name: schedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('schedule_id_seq', 1, false);


--
-- Data for Name: seat; Type: TABLE DATA; Schema: public; Owner: -
--

COPY seat (id, classroom_id, name) FROM stdin;
\.


--
-- Name: seat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('seat_id_seq', 1, false);


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "user" (id, name, gender, telephone, wechat_id, verified, priority) FROM stdin;
\.


--
-- Name: priv_activity_id; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY activity
    ADD CONSTRAINT priv_activity_id PRIMARY KEY (id);


--
-- Name: priv_classroom_id; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY classroom
    ADD CONSTRAINT priv_classroom_id PRIMARY KEY (id);


--
-- Name: priv_schedule_id; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY schedule
    ADD CONSTRAINT priv_schedule_id PRIMARY KEY (id);


--
-- Name: priv_seat_id; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY seat
    ADD CONSTRAINT priv_seat_id PRIMARY KEY (id);


--
-- Name: priv_user_id; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT priv_user_id PRIMARY KEY (id);


--
-- Name: foreign_activity_classroom_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY activity
    ADD CONSTRAINT foreign_activity_classroom_id FOREIGN KEY (classroom_id) REFERENCES classroom(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: foreign_schedule_activity_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY schedule
    ADD CONSTRAINT foreign_schedule_activity_id FOREIGN KEY (activity_id) REFERENCES activity(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: foreign_schedule_seat_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY schedule
    ADD CONSTRAINT foreign_schedule_seat_id FOREIGN KEY (seat_id) REFERENCES seat(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: foreign_schedule_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY schedule
    ADD CONSTRAINT foreign_schedule_user_id FOREIGN KEY (user_id) REFERENCES "user"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: foreign_seat_classroom_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY seat
    ADD CONSTRAINT foreign_seat_classroom_id FOREIGN KEY (classroom_id) REFERENCES classroom(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: public; Type: ACL; Schema: -; Owner: -
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

