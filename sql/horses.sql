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

CREATE SCHEMA main;


ALTER SCHEMA main OWNER TO karisch;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 204 (class 1259 OID 16397)
-- Name: horses; Type: TABLE; Schema: main; Owner: karisch
--

CREATE TABLE main.horses (
    track character varying(200) NOT NULL,
    date character varying(100) NOT NULL,
    race character varying(50) NOT NULL,
    "horseProgram" character varying(50) NOT NULL,
    "horseName" character varying(200),
    "lastRaceDay" character varying(50),
    "lastRaceMonth" character varying(50),
    "lastRaceYear" character varying(50),
    "lastRaceTrack" character varying(50),
    jockey character varying(200),
    weight character varying(50),
    "ME" character varying(100),
    "placePP" character varying(50),
    "placeSeg1" character varying(50),
    "placeSeg2" character varying(50),
    "placeSeg3" character varying(50),
    "placeSeg4" character varying(50),
    "placeSeg5" character varying(50),
    "placeSeg6" character varying(50),
    odds character varying(50),
    comments character varying(300),
    "lastRaceNum" character varying(50),
    "lastRacePlace" character varying(50),
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
    "rlPlaceSeg1" character varying(50),
    "rlPlaceSeg2" character varying(50),
    "rlPlaceSeg3" character varying(50),
    "rlPlaceSeg4" character varying(50),
    "rlPlaceSeg5" character varying(50),
    "rlPlaceSeg6" character varying(50),
    trainer character varying(200),
    owner character varying(200)
);


ALTER TABLE main.horses OWNER TO karisch;

--
-- TOC entry 203 (class 1259 OID 16389)
-- Name: races; Type: TABLE; Schema: main; Owner: karisch
--

CREATE TABLE main.races (
    track character varying(50) NOT NULL,
    date character varying(200) NOT NULL,
    race character varying(100) NOT NULL,
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
    segments character varying(50),
    "fracTime1" character varying(50),
    "fracTime2" character varying(50),
    "fracTime3" character varying(50),
    "fracTime4" character varying(50),
    "fracTime5" character varying(50),
    "finalTime" character varying(50),
    runup character varying(50),
    "wpsPool" character varying(100),
    "firstPlaceWin" character varying(50),
    "firstPlacePlace" character varying(50),
    "firstPlaceShow" character varying(50),
    "secondPlacePlace" character varying(50),
    "secondPlaceShow" character varying(50),
    "thirdPlaceShow" character varying(50),
    "exactaBuyin" character varying(100),
    "exactaFinish" character varying(100),
    "exactaPayout" character varying(100),
    "exactaPool" character varying(100),
    "trifectaBuyin" character varying(100),
    "trifectaFinish" character varying(100),
    "trifectaPayout" character varying(100),
    "trifectaPool" character varying(100)
);


ALTER TABLE main.races OWNER TO karisch;

--
-- TOC entry 2804 (class 2606 OID 16404)
-- Name: horses horses_pkey; Type: CONSTRAINT; Schema: main; Owner: karisch
--

ALTER TABLE ONLY main.horses
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

