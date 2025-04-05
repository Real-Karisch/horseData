--
-- PostgreSQL database dump
--

-- Dumped from database version 12.7 (Ubuntu 12.7-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 13.3

-- Started on 2021-06-22 01:08:26

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 7 (class 2615 OID 16388)
-- Name: main; Type: SCHEMA; Schema: -; Owner: karisch
--

-- CREATE SCHEMA main; -- <<<<<< IF SCHEMA NEEDS TO BE CREATED WILL NEED TO UNCOMMENT THIS!!!!!!!!!


ALTER SCHEMA main OWNER TO karisch;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 204 (class 1259 OID 16397)
-- Name: horses; Type: TABLE; Schema: main; Owner: karisch
--

CREATE TABLE main.horses (
    track character varying(200) NOT NULL,
    date date NOT NULL,
    race smallint NOT NULL,
    "horseProgram" character varying(50) NOT NULL,
    "horseName" character varying(200),
    "lastRaceDay" smallint,
    "lastRaceMonth" character varying(50),
    "lastRaceYear" smallint,
    "lastRaceTrack" character varying(50),
    jockey character varying(200),
    weight smallint,
    "ME" character varying(100),
    "placePP" smallint,
    "placeSeg1" smallint,
    "placeSeg2" smallint,
    "placeSeg3" smallint,
    "placeSeg4" smallint,
    "placeSeg5" smallint,
    "placeSeg6" smallint,
    odds numeric(19,4),
    comments character varying(300),
    "lastRaceNum" smallint,
    "lastRacePlace" smallint,
    "lengthsSeg1" character varying(50),
    "lengthsSeg2" character varying(50),
    "lengthsSeg3" character varying(50),
    "lengthsSeg4" character varying(50),
    "lengthsSeg5" character varying(50),
    "lengthsSeg6" character varying(50),
    "rlLengthsSeg1" character varying(50),
    "rlLengthsSeg2" character varying(50),
    "rlLengthsSeg3" character varying(50),
    "rlLengthsSeg4" character varying(50),
    "rlLengthsSeg5" character varying(50),
    "rlLengthsSeg6" character varying(50),
    "rlPlaceSeg1" smallint,
    "rlPlaceSeg2" smallint,
    "rlPlaceSeg3" smallint,
    "rlPlaceSeg4" smallint,
    "rlPlaceSeg5" smallint,
    "rlPlaceSeg6" smallint,
    trainer character varying(200),
    owner character varying(250)
);


ALTER TABLE main.horses OWNER TO karisch;

--
-- TOC entry 203 (class 1259 OID 16389)
-- Name: races; Type: TABLE; Schema: main; Owner: karisch
--

CREATE TABLE main.races (
    track character varying(50) NOT NULL,
    date date NOT NULL,
    race smallint NOT NULL,
    stakes character varying(100),
    distance character varying(200),
    surface character varying(150),
    weather character varying(200),
    conditions character varying(200),
    "startTime" character varying(50),
    "startNote" character varying(300),
    segment1 character varying(50),
    segment2 character varying(50),
    segment3 character varying(50),
    segment4 character varying(50),
    segment5 character varying(50),
    segments smallint,
    "fracTime1" numeric(19,4),
    "fracTime2" numeric(19,4),
    "fracTime3" numeric(19,4),
    "fracTime4" numeric(19,4),
    "fracTime5" numeric(19,4),
    "finalTime" numeric(19,4),
    runup smallint,
    "wpsPool" int,
    "firstPlaceWin" numeric(19,4),
    "firstPlacePlace" numeric(19,4),
    "firstPlaceShow" numeric(19,4),
    "secondPlacePlace" numeric(19,4),
    "secondPlaceShow" numeric(19,4),
    "thirdPlaceShow" numeric(19,4),
    "exactaBuyin" numeric(19,4),
    "exactaFinish" character varying(100),
    "exactaPayout" numeric(19,4),
    "exactaPool" numeric(19,4),
    "trifectaBuyin" numeric(19,4),
    "trifectaFinish" character varying(100),
    "trifectaPayout" numeric(19,4),
    "trifectaPool" numeric(19,4),
    "superfectaBuyin" numeric(19,4),
    "superfectaFinish" character varying(100),
    "superfectaPayout" numeric(19,4),
    "superfectaPool" numeric(19,4),
    "quinellaBuyin" numeric(19,4),
    "quinellaFinish" character varying(100),
    "quinellaPayout" numeric(19,4),
    "quinellaPool" numeric(19,4)
);


ALTER TABLE main.races OWNER TO karisch;

--
-- TOC entry 2804 (class 2606 OID 16404)
-- Name: horses horses_pkey; Type: CONSTRAINT; Schema: main; Owner: karisch
--

ALTER TABLE main.horses
    ADD CONSTRAINT horses_pkey PRIMARY KEY (track, date, race, "horseProgram");


--
-- TOC entry 2802 (class 2606 OID 16396)
-- Name: races races_pkey; Type: CONSTRAINT; Schema: main; Owner: karisch
--

ALTER TABLE ONLY main.races
    ADD CONSTRAINT races_pkey PRIMARY KEY (track, date, race);


--
-- TOC entry 2805 (class 2606 OID 16405)
-- Name: horses fk_horses_to_races; Type: FK CONSTRAINT; Schema: main; Owner: karisch
--

ALTER TABLE ONLY main.horses
    ADD CONSTRAINT fk_horses_to_races FOREIGN KEY (track, date, race) REFERENCES main.races(track, date, race) NOT VALID;


-- Completed on 2021-06-22 01:08:28

--
-- PostgreSQL database dump complete
--

