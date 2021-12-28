import psycopg2
import time
import csv

# connections ####################################################
db_conn = None
db_cur = None


def ConnectStorage():
    global db_conn
    global db_cur
    while True:
        try:
            db_conn = psycopg2.connect(host="localhost",
                                       port=5432,
                                       dbname="open_drugs",
                                       user="admin",
                                       password="1234"
                                       )
            db_cur = db_conn.cursor()
            db_conn.autocommit = True
            break
        except Exception as e:
            print("db connection error: ", str(e))
            time.sleep(10)


def parse(row: []):
    print(row)

    # 45 Reviewed => none
    reviewed = row[45]
    if not reviewed:
        return

    # 0 # => ?
    # 1  Substance => active_substance.name
    db_cur.execute(f"SELECT get_active_substance_id('{row[1]}');")
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get active_substance rec id")
        return None
    active_substance_id = rec[0]

    # 2  Genetic mutation =>
    # 3  Other genetic intervention =>

    # 4  Organism(name) => species.name => exp.species_id
    db_cur.execute(f"SELECT get_species_id('{row[4]}');")
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get species rec id")
        return None
    species_id = rec[0]

    # 5  Organism(breed) => strain.name => exp.strain_id
    db_cur.execute(f"SELECT get_strain_id('{row[5]}',{species_id});")
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get strain rec id")
        return None
    strain_id = rec[0]

    # 6  Organism(sex) => sex.name => exp.sex_id
    db_cur.execute(f"SELECT get_sex_id('{row[6]}');")
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get sex rec id")
        return None
    sex_id = rec[0]


    # 7  Sample Size(control) =>
    control_size = row[7]

    # 8  Sample Size(experiment) =>
    treatment_size = row[8]

    # 9  Test Site =>
    # 10 Group =>
    # 11 Mean lifespan experiment(days) =>
    # 12 Mean lifespan experiment(%% change) =>
    # 13 Mean lifespan experiment(p-value) =>
    # 14 Median lifespan experiment(days) =>
    # 15 Median lifespan experiment(%% change) =>
    # 16 Median lifespan experiment(p-value) =>
    # 17 Maximal lifespan (90th percentile) experiment(days) =>
    # 18 Maximal lifespan (90th percentile) experiment(%% change) =>
    # 19 Maximal lifespan (90th percentile) experiment(p-value) =>
    # 20 Mean lifespan control =>
    # 21 Median  lifespan control =>
    # 22 Maximal lifespan (or 90th percentile) control =>

    # 23 variables (hours / days / months / ...) => time_unit.name
    db_cur.execute(f"SELECT get_time_unit_id('{row[23]}');")
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get time unit rec id")
        return None
    time_unit_id = rec[0]


    # 24 Way of substance delivery(Option (injection / diet / drink / medium)) =>
    # 25 Way of substance delivery(Mean (water solution / ethanol / DMSO / etc.)) =>
    # 26 Way of substance delivery(Regime (one-time / repeated, for repeated.: continuous / interval)) =>
    # 27 Way of substance delivery(Interval (optional)) =>

    # 28 Concentration(single) =>
    concentraion_single = row[28]

    # 29 Concentration(daily) =>
    # 30 Concentration(summed up) =>

    # 31 The range of substance exposure (% of lifespan)(Start point of treatment) =>
    range_of_subs_expos_1 = row[31]

    # 32 The range of substance exposure (% of lifespan)(Duration of treatment) =>
    range_of_subs_expos_2 = row[32]

    # 33 The range of substance exposure (% of lifespan)(Starting age/end point) =>
    range_of_subs_expos_3 = row[33]

    # 34 Conditions of animal maintenance(quantity of animals/cage) =>
    # 35 Conditions of animal maintenance(temperature) =>

    # 36 Conditions of animal maintenance(feed) =>
    db_cur.execute(f"SELECT get_nutrition_id('{row[36]}');")
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get nutrition rec id")
        return None
    nutrition_id = rec[0]

    # 37 Conditions of animal maintenance(other in control and experiment) =>
    # 38 Conditions of animal maintenance(other in control) =>
    # 39 Conditions of animal maintenance(other in experiment) =>
    #     ---

    # 40 Article(Source) => journal.name => publication.journal_id
    db_cur.execute(f"SELECT get_journal_id('{row[40]}','','');")
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get journal rec id")
        return None
    journal_id = rec[0]

    # publication
    db_cur.execute(f"INSERT INTO publication(doi,pmid,date,journal_id,authors) VALUES ('{row[43]}','{row[44]}','{row[42]}-01-01'::DATE,{journal_id},'') RETURNING id;")
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get publication rec id")
        return None
    publication_id = rec[0]

    # 46 Comment => exp.comment
    comment = row[46]

    # control group
    #     description               TEXT,
    #     control_min_lifespan      NUMERIC,
    #     control_max_lifespan      NUMERIC,
    #     control_median_lifespan   NUMERIC,
    #     lifespan_unit_id          INTEGER REFERENCES time_unit (id) ON DELETE CASCADE,
    #     organisms_density_id      INTEGER REFERENCES organisms_density (id) ON DELETE CASCADE,
    #     survival_plot_source_link TEXT,
    #     survival_plot_coordinates jsonb,
    #     survival_raw_data         jsonb
    db_cur.execute(f'''
    INSERT INTO control_group(description,size)
    VALUES ('',{control_size}) RETURNING id;''')
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get control group rec id")
        return None
    control_group_id = rec[0]

    # experiment
    #     experiment_site_id              INTEGER REFERENCES experiment_site (id) ON DELETE CASCADE,
    #     result_change_max_lifespan      NUMERIC,
    #     result_change_median_lifespan   NUMERIC,
    #     -- temperature_conditions
    #     temperature_condition_range     numrange,
    #     temperature_condition_constance boolean,
    #     -- light_conditions
    #     light_condition_light_hours     NUMERIC,
    #     light_condition_dark_hours      NUMERIC,
    #     -- diet_condition
    #     diet_condition_feed_id          INTEGER,
    #     diet_condition_feed             TEXT,
    #     diet_condition_times_per_day    NUMERIC,
    #     comment                         TEXT
    db_cur.execute(f'''
    INSERT INTO experiment(name,publication_id,species_id,strain_id,sex_id,control_group_id,comment,diet_condition_feed_id)
    VALUES('',{publication_id},{species_id},{strain_id},{sex_id},{control_group_id},'{comment}',{nutrition_id}
    ) RETURNING id;''')
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get experiment rec id")
        return None
    experiment_id = rec[0]

    # treatment_group
    #     survival_plot_data   jsonb,
    #     min_lifespan         NUMERIC,
    #     mean_lifespan        NUMERIC,
    #     median_lifespan      NUMERIC,
    #     max_lifespan         NUMERIC,
    #     organisms_density_id INTEGER REFERENCES organisms_density (id) ON DELETE CASCADE

    db_cur.execute(f'''
    INSERT INTO treatment_group(size,lifespan_unit_id)
    VALUES({treatment_size},{time_unit_id}
    ) RETURNING id;''')
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get experiment rec id")
        return None
    treatment_group_id = rec[0]


    # intervention
    #     intervention_type_id            INTEGER NOT NULL REFERENCES intervention_type (id) ON DELETE CASCADE,
    #     experiment_id                   INTEGER NOT NULL REFERENCES experiment (id) ON DELETE CASCADE,
    #     active_substance_id             INTEGER REFERENCES active_substance (id) ON DELETE CASCADE,
    #     dosage                          NUMERIC,
    #     dosage_unit_id                  INTEGER REFERENCES dosage_unit (id) ON DELETE CASCADE,
    #     start_time                      NUMERIC,
    #     start_time_reference_point_id   INTEGER REFERENCES intervention_period_reference_point (id) ON DELETE CASCADE,
    #     end_time                        NUMERIC,
    #     end_time_reference_point_id     INTEGER REFERENCES intervention_period_reference_point (id) ON DELETE CASCADE,
    #     substance_delivery_way_id       INTEGER REFERENCES substance_delivery_way (id) ON DELETE CASCADE,
    #     substance_delivery_frequency_id INTEGER REFERENCES substance_delivery_frequency (id) ON DELETE CASCADE,
    #     substance_delivery_method       TEXT
    db_cur.execute(f'''
    INSERT INTO intervention(treatment_group_id)
    VALUES({treatment_group_id}
    ) RETURNING id;
    ''')


if __name__ == '__main__':
    print('start')
    ConnectStorage()
    fl = open("./tables/DrugAge_C_Elegans_polina.csv")
    reader = csv.reader(fl)
    for row in reader:
        parse(row)
