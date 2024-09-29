import mysql.connector as c
import pandas as pd
import configparser

def init_database(config, dataset_dir='./data'):
    DF = pd.read_csv(f"{dataset_dir}/{config['dataset']['name']}", sep='\t')

    DB_CONNECTION = c.connect(
        user=config['mysql']['username'],
        password=config['mysql']['password'],
        host=config['mysql']['host'],
        port=config['mysql']['port']
    )

    # PREPARE QUERIES FOR EXECUTION
    CREATE_DB_QUERY = f"CREATE DATABASE IF NOT EXISTS {config['mysql']['database']};"
    USE_DB_QUERY = f"USE {config['mysql']['database']};"
    DROP_TABLE_QUERY = f"DROP TABLE IF EXISTS {config['mysql']['samples_table']};"

    columns_info = ', '.join(list(map(lambda name: f"{name} FLOAT", config['dataset']['features'].split(", "))))
    CREATE_TABLE_QUERY = f"CREATE TABLE IF NOT EXISTS {config['mysql']['samples_table']}({columns_info});"

    row_names = config['dataset']['features'].split(", ")
    stringified_rows = []
    for i in range(DF.shape[0]):
        row_values = []
        for name in row_names:
            row_values.append(str(DF[name][i]))
        stringified_rows.append("(" + ','.join(row_values) + ")")
    INSERT_TABLE_ROWS_QUERY = f"INSERT INTO {config['mysql']['samples_table']}({','.join(row_names)}) VALUES" + ','.join(stringified_rows) + ';'

    # EXECUTING QUERIES
    db_cursor = DB_CONNECTION.cursor()
    db_cursor.execute(CREATE_DB_QUERY)
    db_cursor.execute(USE_DB_QUERY)
    db_cursor.execute(DROP_TABLE_QUERY)
    db_cursor.execute(CREATE_TABLE_QUERY)
    db_cursor.execute(INSERT_TABLE_ROWS_QUERY)

    DB_CONNECTION.commit()
    db_cursor.close()
    DB_CONNECTION.close()

if __name__ == '__main__':
    CONFIG_PATH = './configs/config.ini'
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    init_database(config)