--
-- PostgreSQL database dump
--

-- Dumped from database version 14.0 (Ubuntu 14.0-1.pgdg20.04+1)
-- Dumped by pg_dump version 14.0 (Ubuntu 14.0-1.pgdg20.04+1)

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
-- Name: listcontrols; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA listcontrols;


ALTER SCHEMA listcontrols OWNER TO postgres;

--
-- Name: diet_conditions; Type: TYPE; Schema: listcontrols; Owner: postgres
--

CREATE TYPE listcontrols.diet_conditions AS (
	feed character(1),
	times_per_day numeric,
	feed_id integer
);


ALTER TYPE listcontrols.diet_conditions OWNER TO postgres;

--
-- Name: light_conditions; Type: TYPE; Schema: listcontrols; Owner: postgres
--

CREATE TYPE listcontrols.light_conditions AS (
	light_hours numeric,
	dark_hours numeric
);


ALTER TYPE listcontrols.light_conditions OWNER TO postgres;

--
-- Name: temperatire_conditions; Type: TYPE; Schema: listcontrols; Owner: postgres
--

CREATE TYPE listcontrols.temperatire_conditions AS (
	range numrange,
	constance boolean
);


ALTER TYPE listcontrols.temperatire_conditions OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;


CREATE TABLE listcontrols.control_group (
                                            id integer NOT NULL,
                                            description text,
                                            control_min_lifespan numeric,
                                            control_max_lifespan numeric,
                                            control_median_lifespan numeric,
                                            lifespan_unit_id integer,
                                            organisms_density_id integer,
                                            survival_plot_source_link character(1),
                                            survival_plot_coordinates json,
                                            survival_raw_data json
);


ALTER TABLE listcontrols.control_group OWNER TO postgres;

--
-- Name: dosage_unit; Type: TABLE; Schema: listcontrols; Owner: postgres
--

CREATE TABLE listcontrols.dosage_unit (
                                          id integer NOT NULL,
                                          name character(1) NOT NULL
);


ALTER TABLE listcontrols.dosage_unit OWNER TO postgres;

--
-- Name: drug_target; Type: TABLE; Schema: listcontrols; Owner: postgres
--

CREATE TABLE listcontrols.drug_target (
                                          id integer NOT NULL,
                                          name character(1) NOT NULL
);


ALTER TABLE listcontrols.drug_target OWNER TO postgres;

--
-- Name: experiment; Type: TABLE; Schema: listcontrols; Owner: postgres
--

CREATE TABLE listcontrols.experiment (
                                         id integer NOT NULL,
                                         name character(1),
                                         publication_id integer NOT NULL,
                                         species_id integer NOT NULL,
                                         control_group_id integer,
                                         strain_id integer,
                                         experiment_site_id integer,
                                         result_change_max_lifespan numeric,
                                         result_change_median_lifespan numeric,
                                         sex_id integer,
                                         temperature_conditions listcontrols.temperatire_conditions,
                                         light_conditions listcontrols.light_conditions,
                                         diet_conditions listcontrols.diet_conditions
);


ALTER TABLE listcontrols.experiment OWNER TO postgres;

--
-- Name: experiment_site; Type: TABLE; Schema: listcontrols; Owner: postgres
--

CREATE TABLE listcontrols.experiment_site (
                                              id integer NOT NULL,
                                              name character(1) NOT NULL,
                                              description text
);


ALTER TABLE listcontrols.experiment_site OWNER TO postgres;

--
-- Name: intervention; Type: TABLE; Schema: listcontrols; Owner: postgres
--

CREATE TABLE listcontrols.intervention (
                                           id integer NOT NULL,
                                           intervention_type_id integer NOT NULL,
                                           experiment_id integer NOT NULL,
                                           active_substance_id integer,
                                           dosage numeric,
                                           dosage_unit_id integer,
                                           treatment_group_id integer,
                                           start_time numeric,
                                           start_time_reference_point_id integer,
                                           end_time_reference_point_id integer,
                                           end_time numeric,
                                           substance_delivery_way_id integer,
                                           substance_delivery_frequency_id integer,
                                           substance_delivery_method character(1)
);


ALTER TABLE listcontrols.intervention OWNER TO postgres;

--
-- Name: treatment_group; Type: TABLE; Schema: listcontrols; Owner: postgres
--

CREATE TABLE listcontrols.treatment_group (
                                              id integer NOT NULL,
                                              size integer NOT NULL,
                                              survival_plot_data json,
                                              min_lifespan numeric,
                                              mean_lifespan numeric,
                                              median_lifespan numeric,
                                              max_lifespan numeric,
                                              lifespan_unit_id integer,
                                              organisms_density_id integer
);


ALTER TABLE listcontrols.treatment_group OWNER TO postgres;

--
-- Name: intervention_period_reference_point; Type: TABLE; Schema: listcontrols; Owner: postgres
--

CREATE TABLE listcontrols.intervention_period_reference_point (
                                                                  id integer NOT NULL,
                                                                  name character(1) NOT NULL
);


ALTER TABLE listcontrols.intervention_period_reference_point OWNER TO postgres;

--
-- Name: intervention_type; Type: TABLE; Schema: listcontrols; Owner: postgres
--

CREATE TABLE listcontrols.intervention_type (
                                                id integer NOT NULL,
                                                name character(1) NOT NULL
);


ALTER TABLE listcontrols.intervention_type OWNER TO postgres;

--
-- Name: journal; Type: TABLE; Schema: listcontrols; Owner: postgres
--

CREATE TABLE listcontrols.journal (
                                      id integer NOT NULL,
                                      name character(1) NOT NULL,
                                      link character(1),
                                      rank character(1)
);


ALTER TABLE listcontrols.journal OWNER TO postgres;

--
-- Name: metabolic_enzyme; Type: TABLE; Schema: listcontrols; Owner: postgres
--

CREATE TABLE listcontrols.metabolic_enzyme (
                                               id integer NOT NULL,
                                               name character(1) NOT NULL
);


ALTER TABLE listcontrols.metabolic_enzyme OWNER TO postgres;

--
-- Name: species; Type: TABLE; Schema: listcontrols; Owner: postgres
--

CREATE TABLE listcontrols.species (
                                      id integer NOT NULL,
                                      name character(1) NOT NULL
);


ALTER TABLE listcontrols.species OWNER TO postgres;

--
-- Name: sex; Type: TABLE; Schema: listcontrols; Owner: postgres
--

CREATE TABLE listcontrols.sex (
                                  id integer NOT NULL,
                                  name character(1) NOT NULL
);


ALTER TABLE listcontrols.sex OWNER TO postgres;

--
-- Name: nutrition; Type: TABLE; Schema: listcontrols; Owner: postgres
--

CREATE TABLE listcontrols.nutrition (
                                        id integer NOT NULL,
                                        name character(1) NOT NULL
);


ALTER TABLE listcontrols.nutrition OWNER TO postgres;

--
-- Name: organisms_density; Type: TABLE; Schema: listcontrols; Owner: postgres
--

CREATE TABLE listcontrols.organisms_density (
                                                id integer NOT NULL,
                                                number integer NOT NULL,
                                                area numeric,
                                                area_unit character(1),
                                                constancy boolean
);


ALTER TABLE listcontrols.organisms_density OWNER TO postgres;

--
-- Name: publication; Type: TABLE; Schema: listcontrols; Owner: postgres
--

CREATE TABLE listcontrols.publication (
                                          id integer NOT NULL,
                                          "DOI" character(1),
                                          "PMID" character(1),
                                          date date,
                                          journal_id integer,
                                          authors text
);


ALTER TABLE listcontrols.publication OWNER TO postgres;

--
-- Name: strain; Type: TABLE; Schema: listcontrols; Owner: postgres
--

CREATE TABLE listcontrols.strain (
                                     id integer NOT NULL,
                                     name character(1) NOT NULL,
                                     species_id integer NOT NULL
);


ALTER TABLE listcontrols.strain OWNER TO postgres;

--
-- Name: time_unit; Type: TABLE; Schema: listcontrols; Owner: postgres
--

CREATE TABLE listcontrols.time_unit (
                                        id integer NOT NULL,
                                        name character(1) NOT NULL
);


ALTER TABLE listcontrols.time_unit OWNER TO postgres;

--
-- Name: control_group control_group_pkey; Type: CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.control_group
    ADD CONSTRAINT control_group_pkey PRIMARY KEY (id);


--
-- Name: experiment experiment_pkey; Type: CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.experiment
    ADD CONSTRAINT experiment_pkey PRIMARY KEY (id);


--
-- Name: experiment_site experiment_site_pkey; Type: CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.experiment_site
    ADD CONSTRAINT experiment_site_pkey PRIMARY KEY (id);


--
-- Name: intervention_period_reference_point intervention_period_reference_point_pkey; Type: CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.intervention_period_reference_point
    ADD CONSTRAINT intervention_period_reference_point_pkey PRIMARY KEY (id);


--
-- Name: intervention intervention_pkey; Type: CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.intervention
    ADD CONSTRAINT intervention_pkey PRIMARY KEY (id);


--
-- Name: intervention_type intervention_type_pkey; Type: CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.intervention_type
    ADD CONSTRAINT intervention_type_pkey PRIMARY KEY (id);


--
-- Name: journal journal_pkey; Type: CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.journal
    ADD CONSTRAINT journal_pkey PRIMARY KEY (id);


--
-- Name: metabolic_enzyme metabolic_enzyme_pkey; Type: CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.metabolic_enzyme
    ADD CONSTRAINT metabolic_enzyme_pkey PRIMARY KEY (id);


--
-- Name: species species_pkey; Type: CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.species
    ADD CONSTRAINT species_pkey PRIMARY KEY (id);


--
-- Name: sex sex_pkey; Type: CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.sex
    ADD CONSTRAINT sex_pkey PRIMARY KEY (id);


--
-- Name: nutrition nutrition_pkey; Type: CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.nutrition
    ADD CONSTRAINT nutrition_pkey PRIMARY KEY (id);


--
-- Name: organisms_density organisms_density_pkey; Type: CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.organisms_density
    ADD CONSTRAINT organisms_density_pkey PRIMARY KEY (id);


--
-- Name: publication publication_pkey; Type: CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.publication
    ADD CONSTRAINT publication_pkey PRIMARY KEY (id);


--
-- Name: strain strain_pkey; Type: CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.strain
    ADD CONSTRAINT strain_pkey PRIMARY KEY (id);


--
-- Name: time_unit time_unit_pkey; Type: CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.time_unit
    ADD CONSTRAINT time_unit_pkey PRIMARY KEY (id);

--
-- Name: control_group control_group_lifespan_unit_id_fkey; Type: FK CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.control_group
    ADD CONSTRAINT control_group_lifespan_unit_id_fkey FOREIGN KEY (lifespan_unit_id) REFERENCES listcontrols.time_unit(id) NOT VALID;


--
-- Name: control_group control_group_organisms_density_id_fkey; Type: FK CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.control_group
    ADD CONSTRAINT control_group_organisms_density_id_fkey FOREIGN KEY (organisms_density_id) REFERENCES listcontrols.organisms_density(id) NOT VALID;


--
-- Name: experiment experiment_experiment_site_id_fkey; Type: FK CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.experiment
    ADD CONSTRAINT experiment_experiment_site_id_fkey FOREIGN KEY (experiment_site_id) REFERENCES listcontrols.experiment_site(id) NOT VALID;


--
-- Name: experiment experiment_species_id_fkey; Type: FK CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.experiment
    ADD CONSTRAINT experiment_species_id_fkey FOREIGN KEY (species_id) REFERENCES listcontrols.species(id) NOT VALID;


--
-- Name: experiment experiment_sex_id_fkey; Type: FK CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.experiment
    ADD CONSTRAINT experiment_sex_id_fkey FOREIGN KEY (sex_id) REFERENCES listcontrols.sex(id) NOT VALID;


--
-- Name: experiment experiment_publication_id_fkey; Type: FK CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.experiment
    ADD CONSTRAINT experiment_publication_id_fkey FOREIGN KEY (publication_id) REFERENCES listcontrols.publication(id) NOT VALID;


--
-- Name: experiment experiment_strain_id_fkey; Type: FK CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.experiment
    ADD CONSTRAINT experiment_strain_id_fkey FOREIGN KEY (strain_id) REFERENCES listcontrols.strain(id) NOT VALID;

--
-- Name: intervention intervention_end_time_reference_point_id_fkey; Type: FK CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.intervention
    ADD CONSTRAINT intervention_end_time_reference_point_id_fkey FOREIGN KEY (end_time_reference_point_id) REFERENCES listcontrols.intervention_period_reference_point(id) NOT VALID;


--
-- Name: intervention intervention_experiment_id_fkey; Type: FK CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.intervention
    ADD CONSTRAINT intervention_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES listcontrols.experiment(id) NOT VALID;


--
-- Name: treatment_group treatment_group_lifespan_unit_id_fkey; Type: FK CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.treatment_group
    ADD CONSTRAINT treatment_group_lifespan_unit_id_fkey FOREIGN KEY (lifespan_unit_id) REFERENCES listcontrols.time_unit(id) NOT VALID;


--
-- Name: treatment_group treatment_group_organisms_density_id_fkey; Type: FK CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.treatment_group
    ADD CONSTRAINT treatment_group_organisms_density_id_fkey FOREIGN KEY (organisms_density_id) REFERENCES listcontrols.organisms_density(id) NOT VALID;


--
-- Name: intervention intervention_treatment_group_id_fkey; Type: FK CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.intervention
    ADD CONSTRAINT intervention_treatment_group_id_fkey FOREIGN KEY (treatment_group_id) REFERENCES listcontrols.treatment_group(id) NOT VALID;


--
-- Name: intervention intervention_intervention_type_id_fkey; Type: FK CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.intervention
    ADD CONSTRAINT intervention_intervention_type_id_fkey FOREIGN KEY (intervention_type_id) REFERENCES listcontrols.intervention_type(id) NOT VALID;


--
-- Name: intervention intervention_start_time_reference_point_id_fkey; Type: FK CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.intervention
    ADD CONSTRAINT intervention_start_time_reference_point_id_fkey FOREIGN KEY (start_time_reference_point_id) REFERENCES listcontrols.intervention_period_reference_point(id) NOT VALID;

--
-- Name: publication publication_journal_id_fkey; Type: FK CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.publication
    ADD CONSTRAINT publication_journal_id_fkey FOREIGN KEY (journal_id) REFERENCES listcontrols.journal(id) NOT VALID;


--
-- Name: strain strain_species_id_fkey; Type: FK CONSTRAINT; Schema: listcontrols; Owner: postgres
--

ALTER TABLE ONLY listcontrols.strain
    ADD CONSTRAINT strain_species_id_fkey FOREIGN KEY (species_id) REFERENCES listcontrols.species(id) NOT VALID;

--
-- Name: drug_interventions; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA drug_interventions;


ALTER SCHEMA drug_interventions OWNER TO postgres;

--
-- Name: active_substance; Type: TABLE; Schema: drug_interventions; Owner: postgres
--

CREATE TABLE drug_interventions.active_substance
(
    id   integer      NOT NULL,
    name character(1) NOT NULL
);


ALTER TABLE drug_interventions.active_substance
    OWNER TO postgres;

--
-- Name: active_substance_drug_target; Type: TABLE; Schema: drug_interventions; Owner: postgres
--

CREATE TABLE drug_interventions.active_substance_drug_target
(
    active_substance_id integer NOT NULL,
    drug_target_id      integer NOT NULL
);


ALTER TABLE drug_interventions.active_substance_drug_target
    OWNER TO postgres;

--
-- Name: active_substance_metabolic_enzyme; Type: TABLE; Schema: drug_interventions; Owner: postgres
--

CREATE TABLE drug_interventions.active_substance_metabolic_enzyme
(
    active_substance_id integer NOT NULL,
    metabolic_enzyme_id integer NOT NULL
);


ALTER TABLE drug_interventions.active_substance_metabolic_enzyme
    OWNER TO postgres;

--
-- Name: active_substance_species; Type: TABLE; Schema: drug_interventions; Owner: postgres
--

CREATE TABLE drug_interventions.active_substance_species
(
    active_substance_id                  integer NOT NULL,
    species_id                           integer NOT NULL,
    "half-life_time"                     numrange,
    "half-life_time_unit_id"             integer,
    "half-life_time_elimination"         numrange,
    "half-life_time_elimination_unit_id" integer
);


ALTER TABLE drug_interventions.active_substance_species
    OWNER TO postgres;

--
-- Name: dosage_unit; Type: TABLE; Schema: drug_interventions; Owner: postgres
--

CREATE TABLE drug_interventions.dosage_unit
(
    id   integer      NOT NULL,
    name character(1) NOT NULL
);


ALTER TABLE drug_interventions.dosage_unit
    OWNER TO postgres;

--
-- Name: drug_target; Type: TABLE; Schema: drug_interventions; Owner: postgres
--

CREATE TABLE drug_interventions.drug_target
(
    id   integer      NOT NULL,
    name character(1) NOT NULL
);


ALTER TABLE drug_interventions.drug_target
    OWNER TO postgres;

--
-- Name: experiment; Type: TABLE; Schema: drug_interventions; Owner: postgres
--

CREATE TABLE drug_interventions.experiment
(
    id                            integer NOT NULL,
    name                          character(1),
    publication_id                integer NOT NULL,
    species_id                    integer NOT NULL,
    control_group_id              integer,
    strain_id                     integer,
    experiment_site_id            integer,
    result_change_max_lifespan    numeric,
    result_change_median_lifespan numeric,
    sex_id                        integer,
    temperature_conditions        listcontrols.temperatire_conditions,
    light_conditions              listcontrols.light_conditions,
    diet_conditions               listcontrols.diet_conditions
);


ALTER TABLE drug_interventions.experiment
    OWNER TO postgres;

--
-- Name: intervention; Type: TABLE; Schema: drug_interventions; Owner: postgres
--

CREATE TABLE drug_interventions.intervention
(
    id                              integer NOT NULL,
    intervention_type_id            integer NOT NULL,
    experiment_id                   integer NOT NULL,
    active_substance_id             integer,
    dosage                          numeric,
    dosage_unit_id                  integer,
    treatment_group_id              integer,
    start_time                      numeric,
    start_time_reference_point_id   integer,
    end_time_reference_point_id     integer,
    end_time                        numeric,
    substance_delivery_way_id       integer,
    substance_delivery_frequency_id integer,
    substance_delivery_method       character(1)
);


ALTER TABLE drug_interventions.intervention
    OWNER TO postgres;

--
-- Name: treatment_group; Type: TABLE; Schema: drug_interventions; Owner: postgres
--

CREATE TABLE drug_interventions.treatment_group
(
    id                   integer NOT NULL,
    size                 integer NOT NULL,
    survival_plot_data   json,
    min_lifespan         numeric,
    mean_lifespan        numeric,
    median_lifespan      numeric,
    max_lifespan         numeric,
    lifespan_unit_id     integer,
    organisms_density_id integer
);


ALTER TABLE drug_interventions.treatment_group
    OWNER TO postgres;

--
-- Name: intervention_period_reference_point; Type: TABLE; Schema: drug_interventions; Owner: postgres
--

CREATE TABLE drug_interventions.intervention_period_reference_point
(
    id   integer      NOT NULL,
    name character(1) NOT NULL
);


ALTER TABLE drug_interventions.intervention_period_reference_point
    OWNER TO postgres;

--
-- Name: intervention_type; Type: TABLE; Schema: drug_interventions; Owner: postgres
--

CREATE TABLE drug_interventions.intervention_type
(
    id   integer      NOT NULL,
    name character(1) NOT NULL
);


ALTER TABLE drug_interventions.intervention_type
    OWNER TO postgres;

--
-- Name: metabolic_enzyme; Type: TABLE; Schema: drug_interventions; Owner: postgres
--

CREATE TABLE drug_interventions.metabolic_enzyme
(
    id   integer      NOT NULL,
    name character(1) NOT NULL
);


ALTER TABLE drug_interventions.metabolic_enzyme
    OWNER TO postgres;

--
-- Name: organisms_density; Type: TABLE; Schema: drug_interventions; Owner: postgres
--

CREATE TABLE drug_interventions.organisms_density
(
    id        integer NOT NULL,
    number    integer NOT NULL,
    area      numeric,
    area_unit character(1),
    constancy boolean
);


ALTER TABLE drug_interventions.organisms_density
    OWNER TO postgres;

--
-- Name: publication; Type: TABLE; Schema: drug_interventions; Owner: postgres
--

CREATE TABLE drug_interventions.publication
(
    id         integer NOT NULL,
    "DOI"      character(1),
    "PMID"     character(1),
    date       date,
    journal_id integer,
    authors    text
);


ALTER TABLE drug_interventions.publication
    OWNER TO postgres;

--
-- Name: substance_delivery_frequency; Type: TABLE; Schema: drug_interventions; Owner: postgres
--

CREATE TABLE drug_interventions.substance_delivery_frequency
(
    id   integer      NOT NULL,
    name character(1) NOT NULL
);


ALTER TABLE drug_interventions.substance_delivery_frequency
    OWNER TO postgres;

--
-- Name: substance_delivery_way; Type: TABLE; Schema: drug_interventions; Owner: postgres
--

CREATE TABLE drug_interventions.substance_delivery_way
(
    id   integer      NOT NULL,
    name character(1) NOT NULL
);


ALTER TABLE drug_interventions.substance_delivery_way
    OWNER TO postgres;

--
-- Name: active_substance active_substance_pkey; Type: CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.active_substance
    ADD CONSTRAINT active_substance_pkey PRIMARY KEY (id);


--
-- Name: dosage_unit dosage_unit_pkey; Type: CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.dosage_unit
    ADD CONSTRAINT dosage_unit_pkey PRIMARY KEY (id);


--
-- Name: drug_target drug_target_pkey; Type: CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.drug_target
    ADD CONSTRAINT drug_target_pkey PRIMARY KEY (id);


--
-- Name: experiment experiment_pkey; Type: CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.experiment
    ADD CONSTRAINT experiment_pkey PRIMARY KEY (id);

--
-- Name: treatment_group treatment_group_pkey; Type: CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.treatment_group
    ADD CONSTRAINT treatment_group_pkey PRIMARY KEY (id);


--
-- Name: intervention_period_reference_point intervention_period_reference_point_pkey; Type: CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.intervention_period_reference_point
    ADD CONSTRAINT intervention_period_reference_point_pkey PRIMARY KEY (id);


--
-- Name: intervention intervention_pkey; Type: CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.intervention
    ADD CONSTRAINT intervention_pkey PRIMARY KEY (id);


--
-- Name: intervention_type intervention_type_pkey; Type: CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.intervention_type
    ADD CONSTRAINT intervention_type_pkey PRIMARY KEY (id);

--
-- Name: metabolic_enzyme metabolic_enzyme_pkey; Type: CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.metabolic_enzyme
    ADD CONSTRAINT metabolic_enzyme_pkey PRIMARY KEY (id);

--
-- Name: organisms_density organisms_density_pkey; Type: CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.organisms_density
    ADD CONSTRAINT organisms_density_pkey PRIMARY KEY (id);


--
-- Name: publication publication_pkey; Type: CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.publication
    ADD CONSTRAINT publication_pkey PRIMARY KEY (id);

--
-- Name: substance_delivery_frequency substance_delivery_frequency_pkey; Type: CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.substance_delivery_frequency
    ADD CONSTRAINT substance_delivery_frequency_pkey PRIMARY KEY (id);


--
-- Name: substance_delivery_way substance_delivery_way_pkey; Type: CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.substance_delivery_way
    ADD CONSTRAINT substance_delivery_way_pkey PRIMARY KEY (id);


--
-- Name: active_substance_drug_target active_substance_drug_target_active_substance_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.active_substance_drug_target
    ADD CONSTRAINT active_substance_drug_target_active_substance_id_fkey FOREIGN KEY (active_substance_id) REFERENCES drug_interventions.active_substance (id) NOT VALID;


--
-- Name: active_substance_drug_target active_substance_drug_target_active_substance_id_fkey1; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.active_substance_drug_target
    ADD CONSTRAINT active_substance_drug_target_active_substance_id_fkey1 FOREIGN KEY (active_substance_id) REFERENCES drug_interventions.active_substance (id) NOT VALID;


--
-- Name: active_substance_drug_target active_substance_drug_target_drug_target_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.active_substance_drug_target
    ADD CONSTRAINT active_substance_drug_target_drug_target_id_fkey FOREIGN KEY (drug_target_id) REFERENCES drug_interventions.drug_target (id) NOT VALID;


--
-- Name: active_substance_drug_target active_substance_drug_target_drug_target_id_fkey1; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.active_substance_drug_target
    ADD CONSTRAINT active_substance_drug_target_drug_target_id_fkey1 FOREIGN KEY (drug_target_id) REFERENCES drug_interventions.drug_target (id) NOT VALID;


--
-- Name: active_substance_metabolic_enzyme active_substance_metabolic_enzyme_active_substance_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.active_substance_metabolic_enzyme
    ADD CONSTRAINT active_substance_metabolic_enzyme_active_substance_id_fkey FOREIGN KEY (active_substance_id) REFERENCES drug_interventions.active_substance (id) NOT VALID;


--
-- Name: active_substance_metabolic_enzyme active_substance_metabolic_enzyme_metabolic_enzyme_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.active_substance_metabolic_enzyme
    ADD CONSTRAINT active_substance_metabolic_enzyme_metabolic_enzyme_id_fkey FOREIGN KEY (metabolic_enzyme_id) REFERENCES drug_interventions.metabolic_enzyme (id) NOT VALID;


--
-- Name: active_substance_species active_substance_model_organi_half-life_time_elimination_u_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.active_substance_species
    ADD CONSTRAINT "active_substance_model_organi_half-life_time_elimination_u_fkey" FOREIGN KEY ("half-life_time_elimination_unit_id") REFERENCES listcontrols.time_unit (id) NOT VALID;


--
-- Name: active_substance_species active_substance_species_active_substance_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.active_substance_species
    ADD CONSTRAINT active_substance_species_active_substance_id_fkey FOREIGN KEY (active_substance_id) REFERENCES drug_interventions.active_substance (id) NOT VALID;


--
-- Name: active_substance_species active_substance_species_half-life_time_unit_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.active_substance_species
    ADD CONSTRAINT "active_substance_species_half-life_time_unit_id_fkey" FOREIGN KEY ("half-life_time_unit_id") REFERENCES listcontrols.time_unit (id) NOT VALID;


--
-- Name: active_substance_species active_substance_species_species_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.active_substance_species
    ADD CONSTRAINT active_substance_species_species_id_fkey FOREIGN KEY (species_id) REFERENCES listcontrols.species (id) NOT VALID;

--
-- Name: experiment experiment_publication_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.experiment
    ADD CONSTRAINT experiment_publication_id_fkey FOREIGN KEY (publication_id) REFERENCES drug_interventions.publication (id) NOT VALID;


--
-- Name: experiment experiment_strain_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.experiment
    ADD CONSTRAINT experiment_strain_id_fkey FOREIGN KEY (strain_id) REFERENCES listcontrols.strain (id) NOT VALID;


--
-- Name: intervention intervention_active_substance_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.intervention
    ADD CONSTRAINT intervention_active_substance_id_fkey FOREIGN KEY (active_substance_id) REFERENCES drug_interventions.active_substance (id) NOT VALID;


--
-- Name: intervention intervention_dosage_unit_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.intervention
    ADD CONSTRAINT intervention_dosage_unit_id_fkey FOREIGN KEY (dosage_unit_id) REFERENCES drug_interventions.dosage_unit (id) NOT VALID;


--
-- Name: intervention intervention_end_time_reference_point_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.intervention
    ADD CONSTRAINT intervention_end_time_reference_point_id_fkey FOREIGN KEY (end_time_reference_point_id) REFERENCES drug_interventions.intervention_period_reference_point (id) NOT VALID;


--
-- Name: intervention intervention_experiment_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.intervention
    ADD CONSTRAINT intervention_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES drug_interventions.experiment (id) NOT VALID;


--
-- Name: treatment_group treatment_group_lifespan_unit_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.treatment_group
    ADD CONSTRAINT treatment_group_lifespan_unit_id_fkey FOREIGN KEY (lifespan_unit_id) REFERENCES listcontrols.time_unit (id) NOT VALID;


--
-- Name: treatment_group treatment_group_organisms_density_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.treatment_group
    ADD CONSTRAINT treatment_group_organisms_density_id_fkey FOREIGN KEY (organisms_density_id) REFERENCES drug_interventions.organisms_density (id) NOT VALID;


--
-- Name: intervention intervention_treatment_group_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.intervention
    ADD CONSTRAINT intervention_treatment_group_id_fkey FOREIGN KEY (treatment_group_id) REFERENCES drug_interventions.treatment_group (id) NOT VALID;


--
-- Name: intervention intervention_intervention_type_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.intervention
    ADD CONSTRAINT intervention_intervention_type_id_fkey FOREIGN KEY (intervention_type_id) REFERENCES drug_interventions.intervention_type (id) NOT VALID;


--
-- Name: intervention intervention_start_time_reference_point_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.intervention
    ADD CONSTRAINT intervention_start_time_reference_point_id_fkey FOREIGN KEY (start_time_reference_point_id) REFERENCES drug_interventions.intervention_period_reference_point (id) NOT VALID;


--
-- Name: intervention intervention_substance_delivery_frequency_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.intervention
    ADD CONSTRAINT intervention_substance_delivery_frequency_id_fkey FOREIGN KEY (substance_delivery_frequency_id) REFERENCES drug_interventions.substance_delivery_frequency (id) NOT VALID;


--
-- Name: intervention intervention_substance_delivery_way_id_fkey; Type: FK CONSTRAINT; Schema: drug_interventions; Owner: postgres
--

ALTER TABLE ONLY drug_interventions.intervention
    ADD CONSTRAINT intervention_substance_delivery_way_id_fkey FOREIGN KEY (substance_delivery_way_id) REFERENCES drug_interventions.substance_delivery_way (id) NOT VALID;

--
-- PostgreSQL database dump complete
--

