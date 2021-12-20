from config import CONFIG
from entities import entities

import psycopg2


class BaseDAO:
    connection = None

    def __init__(self):
        if self.connection is None:
            # migrations
            connstr = CONFIG['DB_CONN']
            import subprocess
            args = ["yoyo", "apply", "--database", connstr, "-b", "./db/migrations"]
            subprocess.run(args)

            # conn
            self.connection = psycopg2.connect(connstr
                # host=host, port=port, user=user, password=password, database=database,
            )
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
        cur = self.cnx.cursor(dictionary=True)
        cur.execute('SET SESSION group_concat_max_len = 100000;')
        cur.execute(request)
        return cur.fetchall()

    def get(self, id: int = None) -> entities.Experiment:
        cur = self.cnx.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM `experiment` WHERE id= %(id)s;",
            {'id': id},
        )
        result = cur.fetchone()
        return result

    def add(self, experiment: entities.Experiment) -> entities.Experiment:
        '''
        :param experiment:
        :return:
        '''
        experiment_dict = experiment.dict(exclude_none=True)

        # It's OK to use f-strings, because of Pydantic validation.
        query = f"INSERT INTO `experiment` ({', '.join(experiment_dict.keys())}) "
        subs = ', '.join([f'%({k})s' for k in experiment_dict.keys()])
        query += f"VALUES ({subs});"

        cur = self.cnx.cursor(dictionary=True)
        cur.execute(query, experiment_dict)
        self.cnx.commit()

        cur.execute(
            "SELECT * FROM experiment WHERE ID=%(id)s;",
            {'id': cur.lastrowid},
        )
        result = cur.fetchone()
        self.cnx.close()

        return result

    def update(self, experiment: entities.Experiment, ) -> entities.Experiment:
        experiment_dict = experiment.dict(exclude_none=True)
        prep_str = [f"`{k}` = %({k})s" for k in experiment_dict.keys()]

        query = f"""
            UPDATE experiment
            SET {', '.join(prep_str)}
            WHERE id={experiment_dict['id']};
        """

        cur = self.cnx.cursor(dictionary=True)
        cur.execute(query, experiment_dict)
        self.cnx.commit()
        cur.close()

        return self.get(id=experiment_dict['id'])
