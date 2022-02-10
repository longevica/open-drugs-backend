from config import CONFIG
from entities.experiment import Experiment

import psycopg2


class BaseDAO:
    connection = None

    def __init__(self):
        if self.connection is None:
            # migrations
            connection_config = CONFIG['DB_CONN']
            import subprocess
            args = ["yoyo", "apply", "--database", connection_config, "-b", "./db/migrations"]
            subprocess.run(args)

            # conn
            self.connection = psycopg2.connect(connection_config)
            cursor = self.connection.cursor()
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("success connected - ", record, "\n")
            cursor.close()
        # cursor
        self.cursor = self.connection.cursor()


class ExperimentDAO(BaseDAO):
    """Experiment table fetcher."""

    def get_list(self, request):
        cur = self.connection.cursor()
        query = """
            select experiment.id, strain.id, strain.name, sex.name, 
            treatment_group.max_lifespan, treatment_group.min_lifespan, treatment_group.median_lifespan, 
            lifespan_unit.name, 
            active_substance.name
            from experiment
            JOIN intervention ON intervention.experiment_id = experiment.id
            JOIN treatment_group ON intervention.treatment_group_id = treatment_group.id
            JOIN strain ON experiment.strain_id = strain.id
            JOIN sex ON experiment.sex_id = sex.id
            JOIN time_unit lifespan_unit ON treatment_group.lifespan_unit_id = lifespan_unit.id 
            LEFT JOIN active_substance ON intervention.active_substance_id = active_substance.id 
        """
        cur.execute(query)
        return cur.fetchall()

    def get(self, id: int = None) -> Experiment:
        cur = self.connection.cursor()
        cur.execute(
            "SELECT * FROM experiment WHERE id= %(id)s;",
            {'id': id},
        )
        result = cur.fetchone()
        return result

    def add(self, experiment: Experiment) -> Experiment:
        """
        :param experiment:
        :return:
        """
        experiment_dict = experiment.dict(exclude_none=True)

        # It's OK to use f-strings, because of Pydantic validation.
        query = f"INSERT INTO `experiment` ({', '.join(experiment_dict.keys())}) "
        subs = ', '.join([f'%({k})s' for k in experiment_dict.keys()])
        query += f"VALUES ({subs});"

        cur = self.connection.cursor(dictionary=True)
        cur.execute(query, experiment_dict)
        self.connection.commit()

        cur.execute(
            "SELECT * FROM experiment WHERE ID=%(id)s;",
            {'id': cur.lastrowid},
        )
        result = cur.fetchone()
        self.connection.close()

        return result

    def update(self, experiment: Experiment, ) -> Experiment:
        experiment_dict = experiment.dict(exclude_none=True)
        prep_str = [f"`{k}` = %({k})s" for k in experiment_dict.keys()]

        query = f"""
            UPDATE experiment
            SET {', '.join(prep_str)}
            WHERE id={experiment_dict['id']};
        """

        cur = self.connection.cursor(dictionary=True)
        cur.execute(query, experiment_dict)
        self.connection.commit()
        cur.close()

        return self.get(id=experiment_dict['id'])
