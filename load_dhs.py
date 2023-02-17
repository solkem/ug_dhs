import psycopg2.extras as extras
import json
from shapely.geometry import shape
from shapely.wkb import dumps
import psycopg2

def load_dhs(dhs_df, db_config):
    """Load the transformed data into Postgres"""
    print(dhs_df)
    # Create the database connection
    
    conn = psycopg2.connect(
        host=db_config["hostname"],
        port=db_config["port"],
        user=db_config["username"],
        password=db_config["password"],
        database=db_config["database"]
    )
    
    

    # Load data into the ug_dhs_2016 table
    dhs_df_tuples = [tuple(x) for x in dhs_df.to_numpy()]
    cols = ','.join(list(dhs_df.columns))
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS ug_dhs_2016")
        cur.execute("""
                    CREATE TABLE ug_dhs_2016 (
                        v001 INTEGER NOT NULL,
                        v002 INTEGER NOT NULL,
                        v003 INTEGER NOT NULL,
                        v012 INTEGER,
                        v133 INTEGER,
                        v535 BOOLEAN,
                        v751 BOOLEAN,
                        adult_radio_regular BOOLEAN,
                        sex VARCHAR
                    )
                """)
        sql = "INSERT INTO %s(%s) VALUES %%s" % ('ug_dhs_2016', cols)
        extras.execute_values(cur, sql, dhs_df_tuples)
        conn.commit()
