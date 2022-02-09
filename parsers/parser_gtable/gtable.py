import psycopg2
import time
import csv

# connections ####################################################
db_conn = None
db_cur = None

NA = 'n/a'

tu_day = 'day'
tu_hour = 'hour'

time_unit_assoc = {
    'day':tu_day,
    'days':tu_day,
    'd':tu_day,
    'hour':tu_hour,
    'hours':tu_hour,
    'h':tu_hour
}

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

def get_time_unit(unit)->int:
    dunit = time_unit_assoc.get(unit)
    if dunit is None:
        dunit = unit
    db_cur.execute(f"SELECT get_time_unit_id('{dunit}');")
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get time unit rec id")
        return None
    return rec[0]

def handle_empty_value(val):
    if val == '':
        val = '0'
    return val

def handle_real_number(val:str):
    return val.strip().replace(',', '.')

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
    test_site = row[9]
    if not test_site:
        test_site = NA
    db_cur.execute(f"SELECT get_experiment_site_id('{test_site}','');")
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err test site rec id")
        return None
    exp_site_id = rec[0]


    # 10 Group =>
    # 11 Mean lifespan experiment(days) =>
    mean_lspan_exp = handle_empty_value(row[11].strip().replace(',','.'))


    # 12 Mean lifespan experiment(%% change) =>
    mean_lspan_exp_percent = str(row[12]).strip().replace(',','.')
    mean_lspan_exp_percent = handle_empty_value(mean_lspan_exp_percent.replace('%','').strip())

    # 13 Mean lifespan experiment(p-value) =>

    # 14 Median lifespan experiment(days) =>
    median_lspan_exp = handle_empty_value(row[14].strip().replace(',','.'))

    # 15 Median lifespan experiment(%% change) =>
    median_lspan_exp_percent = handle_empty_value(row[15].strip().replace(',','.'))
    median_lspan_exp_percent = median_lspan_exp_percent.replace('%','').strip()

    # 16 Median lifespan experiment(p-value) =>

    # 17 Maximal lifespan (90th percentile) experiment(days) =>
    maximal_lspan_exp = handle_empty_value(row[17].strip().replace(',','.'))

    # 18 Maximal lifespan (90th percentile) experiment(%% change) =>
    maximal_lspan_exp_percent = handle_empty_value(row[18].strip().replace(',','.'))
    maximal_lspan_exp_percent = maximal_lspan_exp_percent.replace('%','').strip()

    # 19 Maximal lifespan (90th percentile) experiment(p-value) =>

    # 20 Mean lifespan control =>
    mean_lspan_control = handle_empty_value(row[20].strip())
    mean_lspan_control = mean_lspan_control.replace(',','.')

    # 21 Median  lifespan control =>
    median_lspan_control = handle_empty_value(row[21].strip().replace(',','.'))

    # 22 Maximal lifespan (or 90th percentile) control =>
    maximal_lspan_control = handle_empty_value(row[22].strip().replace(',','.'))

    # 23 variables (hours / days / months / ...) => time_unit.name
    time_unit_id = get_time_unit(row[23].strip())

    # 24 Way of substance delivery(Option (injection / diet / drink / medium)) =>
    db_cur.execute(f"SELECT get_substance_delivery_way_id('{row[24].strip()}');")
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get substance_delivery_way rec id")
        return None
    substance_delivery_way_id = rec[0]

    # 25 Way of substance delivery(Mean (water solution / ethanol / DMSO / etc.)) =>
    way_substance_method = row[25]

    # 26 Way of substance delivery(Regime (one-time / repeated, for repeated.: continuous / interval)) =>
    db_cur.execute(f"SELECT get_substance_delivery_frequency_id('{row[26].strip()}');")
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get substance_delivery_frequency rec id")
        return None
    way_substance_frequency_id = rec[0]

    # 27 Way of substance delivery(Interval (optional)) =>
    way_substance_delivery_interval = row[27].strip()


    # 28 Concentration(single) =>
    concentraion_single_ls = row[28].strip().split(" ")
    if len(concentraion_single_ls) == 2:
        concentration_dosage = concentraion_single_ls[0].strip().replace(',','.')
        concentration_dosage_unit = concentraion_single_ls[1].strip()
    else:
        split_idx = 0
        for l in row[28].strip():
            if l.isdigit():
                split_idx += 1
            else:
                concentration_dosage = row[28][0:split_idx].strip().replace(',','.')
                concentration_dosage_unit = row[28][split_idx:].strip()
                break

    db_cur.execute(f"SELECT get_dosage_unit_id('{concentration_dosage_unit}');")
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get concentration_dosage_unit rec id")
        return None
    concentration_dosage_unit_id = rec[0]


    # 29 Concentration(daily) =>
    # 30 Concentration(summed up) =>

    # 31 The range of substance exposure (% of lifespan)(Start point of treatment) =>
    range_of_subs_expos_1 = row[31]

    # 32 The range of substance exposure (% of lifespan)(Duration of treatment) =>
    range_of_subs_expos_2 = row[32]

    # 33 The range of substance exposure (% of lifespan)(Starting age/end point) =>
    range_of_subs_expos_3 = row[33]

    # 34 Conditions of animal maintenance(quantity of animals/cage) =>
    condition_quantity_of_animals = row[34]

    # 35 Conditions of animal maintenance(temperature) =>
    condition_temperature = row[35]

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

    # ###################################################################################
    # publication
    db_cur.execute(f"INSERT INTO publication(doi,pmid,date,journal_id,authors) VALUES ('{row[43]}','{row[44]}','{row[42]}-01-01'::DATE,{journal_id},'') RETURNING id;")
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get publication rec id")
        return None
    publication_id = rec[0]

    # 46 Comment => exp.comment
    comment = row[46]

    # ###################################################################################
    # organisms_density
    #     area      NUMERIC,
    #     area_unit TEXT,
    if not condition_quantity_of_animals:
        condition_quantity_of_animals = 0
    db_cur.execute(f'''SELECT get_organisms_density_id({condition_quantity_of_animals},'0.0','',TRUE);''')
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get density rec id")
        return None
    organisms_density_id = rec[0]

    # ###################################################################################
    condition_temperature = condition_temperature.replace('°C','').strip()
    condition_temperature_numrange = f'numrange({condition_temperature}-0.01,{condition_temperature})'
    condition_temperature_constance = 'TRUE'
    if '–' in condition_temperature:
        ls = condition_temperature.strip('–')
        temp_begin = ls[0].strip()
        temp_end = ls[1].strip()
        condition_temperature_numrange = f'numrange({temp_begin},{temp_end})'
        condition_temperature_constance = 'FALSE'

    # experiment
    #     -- light_conditions
    #     light_condition_light_hours     NUMERIC,
    #     light_condition_dark_hours      NUMERIC,
    #     -- diet_condition
    #     diet_condition_feed             TEXT,
    #     diet_condition_times_per_day    NUMERIC,
    db_cur.execute(f'''
    INSERT INTO experiment(name,publication_id,species_id,strain_id,sex_id,
    comment,diet_condition_feed_id,experiment_site_id,
    result_change_max_lifespan,result_change_median_lifespan,
    temperature_condition_range,temperature_condition_constance 
    )
    VALUES('',{publication_id},{species_id},{strain_id},{sex_id},
    '{comment}',{nutrition_id},{exp_site_id},'{maximal_lspan_exp_percent}','{median_lspan_exp_percent}',
    {condition_temperature_numrange}, {condition_temperature_constance}
    ) RETURNING id;''')
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get experiment rec id")
        return None
    experiment_id = rec[0]

    # ###################################################################################
    # control group
    #     description               TEXT,
    #     control_min_lifespan      NUMERIC,
    #     survival_plot_source_link TEXT,
    #     survival_plot_coordinates jsonb,
    #     survival_raw_data         jsonb
    db_cur.execute(f'''
    INSERT INTO control_group(description,size,control_mean_lifespan,
    control_median_lifespan,control_max_lifespan,lifespan_unit_id,
    organisms_density_id,experiment_id)
    VALUES ('',{control_size},'{mean_lspan_control}','{median_lspan_control}',
    '{maximal_lspan_control}',{time_unit_id},{organisms_density_id},{experiment_id}) RETURNING id;''')
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get control group rec id")
        return None
    control_group_id = rec[0]

    # ###################################################################################
    # treatment_group
    #     survival_plot_data   jsonb,
    #     min_lifespan         NUMERIC,
    db_cur.execute(f'''
    INSERT INTO treatment_group(size,lifespan_unit_id,mean_lifespan, median_lifespan,
    max_lifespan,organisms_density_id,experiment_id)
    VALUES({treatment_size},{time_unit_id},'{mean_lspan_exp}','{median_lspan_exp}',
    '{maximal_lspan_exp}',{organisms_density_id},{experiment_id}) RETURNING id;''')
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get experiment rec id")
        return None
    treatment_group_id = rec[0]



    # intervention type
    intervention_type_name = 'drug'
    db_cur.execute(f"SELECT get_intervention_type_id('{intervention_type_name}');")
    rec = db_cur.fetchone()
    if rec is None or len(rec) == 0:
        print("err get intervention_type rec id")
        return None
    intervention_type_id = rec[0]


# ###################################################################################
    # intervention
    #     start_time                      NUMERIC,
    #     start_time_reference_point_id   INTEGER REFERENCES intervention_period_reference_point (id) ON DELETE CASCADE,
    #     end_time                        NUMERIC,
    #     end_time_reference_point_id     INTEGER REFERENCES intervention_period_reference_point (id) ON DELETE CASCADE,
    db_cur.execute(f'''
    INSERT INTO intervention(intervention_type_id,treatment_group_id,active_substance_id,experiment_id, 
        substance_delivery_way_id, substance_delivery_frequency_id, substance_delivery_method,
        dosage,dosage_unit_id)
    VALUES({intervention_type_id},{treatment_group_id},{active_substance_id},{experiment_id},
    {substance_delivery_way_id},{way_substance_frequency_id},'{way_substance_method}',
    '{concentration_dosage}',{concentration_dosage_unit_id}
    ) RETURNING id;
    ''')

if __name__ == '__main__':
    print('start')
    ConnectStorage()
    fl = open("./tables/DrugAge_C_Elegans_polina.csv")
    reader = csv.reader(fl)
    for row in reader:
        parse(row)
