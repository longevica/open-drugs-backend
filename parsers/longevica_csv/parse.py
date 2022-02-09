import psycopg2
import time
import csv
import statistics
import json
from config import CONFIG

# connections ####################################################
db_conn = None
db_cur = None


def connect_storage():
    global db_conn
    global db_cur
    while True:
        try:
            db_conn = psycopg2.connect(host=CONFIG['DB_HOST'],
                                       port=CONFIG['DB_PORT'],
                                       dbname=CONFIG['DB_NAME'],
                                       user=CONFIG['DB_USER'],
                                       password=CONFIG['DB_PASS']
                                       )
            db_cur = db_conn.cursor()
            db_conn.autocommit = True
            break
        except Exception as e:
            print("db connection error: ", str(e))
            time.sleep(10)


def insert_csv_substances():
    file = open("data/active_substance.csv")
    reader = csv.reader(file)
    for row in reader:
        print(row)
        db_cur.execute("""
                INSERT INTO active_substance(
                    id,
                    name,
                    aliases,
                    pubchem_id,
                    chembl_id,
                    chebi_id,
                    kegg_comp_id,
                    kegg_drug_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])


def parse_substances():
    file = open("data/dbases-ids.csv")
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        print(row)
        id = row[0]
        names = row[1].split(', ')
        name = names[0]
        aliases = names
        pubchem_ids = row[2].split(', ')
        chembl_ids = row[3].split(', ')
        chebi_ids = row[4].split(', ')
        kegg_comp_ids = row[6].split(', ')
        kegg_drug_ids = row[8].split(', ')
        print(names)
        db_cur.execute(
            "SELECT get_active_substance_id(%s, %s::text[], %s::text[], %s::text[], %s::text[], %s::text[], %s::text[])",
            [name, aliases, pubchem_ids, chembl_ids, chebi_ids, kegg_comp_ids, kegg_drug_ids])
        rec = db_cur.fetchone()
        print(rec)


def parse_controls():
    file = open("data/controls.csv")
    lines = file.readlines()
    file.close()
    control_female = list(map(int, lines[0].split(',')))
    control_male = list(map(int, lines[2].split(',')))
    diet_female = list(map(int, lines[1].split(',')))
    diet_male = list(map(int, lines[3].split(',')))
    db_cur.execute("SELECT get_time_unit_id('days');")
    time_unit_id = db_cur.fetchone()[0]
    db_cur.execute("SELECT get_sex_id('female');")
    female_sex_id = db_cur.fetchone()[0]
    db_cur.execute("SELECT get_sex_id('male');")
    male_sex_id = db_cur.fetchone()[0]
    insert_control(control_female, 'Female mice', time_unit_id)  # 1 row
    insert_control(control_male, 'Male mice', time_unit_id)  # 2 row

    insert_diet_intervention(diet_female, 1, female_sex_id)
    insert_diet_intervention(diet_male, 2, male_sex_id)


def insert_control(control_data, description, time_unit_id):
    db_cur.execute(f'''SELECT get_organisms_density_id(5,'0.0','',TRUE);''')
    organisms_density_id = db_cur.fetchone()[0]
    db_cur.execute(f"""
            INSERT INTO control_group(
                size,
                description,
                min_lifespan,
                max_lifespan,
                median_lifespan,
                mean_lifespan,
                lifespan_unit_id,
                organisms_density_id,
                survival_raw_data
            )
            VALUES (
            {len(control_data)},
            '{description}',
            {min(control_data)},
            {max(control_data)},
            {statistics.median(control_data)},
            {statistics.mean(control_data)},
            {time_unit_id},
            {organisms_density_id},
            '{json.dumps(control_data)}'
            ) RETURNING id;
        """)


def insert_experiment(control_group_id, sex_id):
    db_cur.execute(f"SELECT get_species_id('mus musculus');")
    species_id = db_cur.fetchone()[0]
    db_cur.execute(f"SELECT get_strain_id('B6C3F1/J',{species_id});")
    strain_id = db_cur.fetchone()[0]
    db_cur.execute(f"""
                    INSERT INTO experiment(
                        description,
                        publication_id, 
                        species_id, 
                        control_group_id, 
                        strain_id,  
                        sex_id,
                        observation_start_time,
                        diet_condition_feed
--                         result_change_max_lifespan, 
--                         result_change_median_lifespan,
                    )
                    VALUES (
                    'Longevica interventions testing',
                    null,
                    {species_id},
                    {control_group_id},
                    {strain_id},
                    {sex_id},
                    0,
                    'AIN-93M'
                    ) RETURNING id;
                """)
    return db_cur.fetchone()[0]


def insert_diet_intervention(diet_data, control_group_id, sex_id):
    db_cur.execute("SELECT get_intervention_type_id('diet');")
    diet_type_id = db_cur.fetchone()[0]
    db_cur.execute("SELECT get_intervention_period_reference_point_id('from birth');")
    reference_point_id = db_cur.fetchone()[0]
    experiment_id = insert_experiment(control_group_id, sex_id)
    treatment_group_id = insert_treatment_group(diet_data)
    db_cur.execute(f"""
                INSERT INTO intervention(
                    intervention_type_id, 
                    experiment_id, 
                    treatment_group_id,
                    start_time,
                    start_time_reference_point_id, 
                    end_time,
                    end_time_reference_point_id,
                    description
                )
                VALUES (
                {diet_type_id},
                {experiment_id},
                {treatment_group_id},
                120,
                {reference_point_id},
                0,
                {reference_point_id},
                'Dietary restriction diet (60% of ad libitum)'
                ) RETURNING id;
            """)


def insert_drug_intervention(active_substance_id, dosage, dosage_unit_id, survival_data, control_group_id, sex_id, description):
    db_cur.execute("SELECT get_intervention_type_id('drug');")
    diet_type_id = db_cur.fetchone()[0]
    db_cur.execute("SELECT get_intervention_period_reference_point_id('from birth');")
    reference_point_id = db_cur.fetchone()[0]
    experiment_id = insert_experiment(control_group_id, sex_id)
    treatment_group_id = insert_treatment_group(survival_data)
    db_cur.execute("""INSERT INTO intervention(
                    intervention_type_id, 
                    experiment_id, 
                    active_substance_id, 
                    dosage, 
                    dosage_unit_id, 
                    treatment_group_id,
                    start_time,
                    start_time_reference_point_id, 
                    end_time,
                    end_time_reference_point_id,
                    description
                )
                VALUES (%s, %s, %s, %s, %s, %s, 120, %s, 0, %s, %s) RETURNING id;
            """, [diet_type_id, experiment_id, active_substance_id, dosage, dosage_unit_id, treatment_group_id,
                  reference_point_id, reference_point_id, description])


def insert_treatment_group(treatment_data):
    db_cur.execute("SELECT get_time_unit_id('days');")
    time_unit_id = db_cur.fetchone()[0]
    db_cur.execute(f'''SELECT get_organisms_density_id(5,'0.0','',TRUE);''')
    organisms_density_id = db_cur.fetchone()[0]
    db_cur.execute(f"""
                INSERT INTO treatment_group(
                    size,
                    min_lifespan,
                    max_lifespan,
                    median_lifespan,
                    mean_lifespan,
                    lifespan_unit_id,
                    organisms_density_id,
                    survival_raw_data
                )
                VALUES (
                {len(treatment_data)},
                {min(treatment_data)},
                {max(treatment_data)},
                {statistics.median(treatment_data)},
                {statistics.mean(treatment_data)},
                {time_unit_id},
                {organisms_density_id},
                '{json.dumps(treatment_data)}'
                ) RETURNING id;
            """)
    return db_cur.fetchone()[0]


def parse_drug_experiments():
    file = open("data/keySurvivalCurveData.csv")
    reader = csv.reader(file)
    db_cur.execute("SELECT get_sex_id('female');")
    female_sex_id = db_cur.fetchone()[0]
    db_cur.execute("SELECT get_dosage_unit_id('mg/kg/day');")
    dosage_unit_id = db_cur.fetchone()[0]
    dosage_file = open("data/dosage_weight.csv")
    dosage_data = list(csv.reader(dosage_file, delimiter=';'))

    for row in reader:
        id = int(row[0])
        db_cur.execute(f"SELECT name from active_substance where id={id};")
        active_substance_name = db_cur.fetchone()[0]
        dosage_original = dosage_data[id][1]
        print(dosage_original)
        dosage = ((float(dosage_original) / 330.0) * 5.0) / 0.025
        description = f"{active_substance_name} {dosage} mg/kg/day treatment"
        survival_data = list(map(int, row[1:]))
        insert_drug_intervention(id, dosage, dosage_unit_id, survival_data, 1, female_sex_id, description)


if __name__ == '__main__':
    print('start')
    connect_storage()
    insert_csv_substances()
    # parse_controls()
    parse_drug_experiments()

