import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus
load_dotenv()
def get_engine():
    user = os.getenv("DB_USER")
    password = quote_plus(os.getenv("DB_PASSWORD"))
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")

    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"

    print("DB URL =", url)

    return create_engine(url)

def load_dataframe(df, table_name, engine):
    try:
        df.to_sql(
            table_name,
            engine,
            if_exists='replace',   
            index=False,
            chunksize=1000
        )
        print(f"{len(df)} lignes chargées dans '{table_name}'")
    except Exception as e:
        print(f"Erreur lors du chargement de '{table_name}' : {e}")

def test_connection(engine):
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            print(f"Connexion PostgreSQL OK : {result.fetchone()[0]}")
    except Exception as e:
        print(f"Connexion échouée : {e}")