import sys
import os
# C:\Users\aneme\vscode\publicConsulationScrap
module_path = os.path.abspath(os.path.join('.'))
print(module_path)
# add public consultation folder to import search paths
if module_path not in sys.path:
    sys.path.append(module_path)
    
from text_utils.helpers import numpy_to_db, db_to_numpy
from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import numpy as np



def test_numpy_to_db():
    config = ConfigParser()
    config.read("config.ini")
    db_file = config.get('DEFAULT', 'db_file')
    engine = create_engine(db_file)
    articleId = -1
    vector = np.random.rand(100)
    with engine.connect() as conn:
        params = {}
        params["id"] = articleId
        conn.execute(text("""DELETE FROM ArticleEmbeddings WHERE articleId = :id"""), params)
        conn.commit()
        numpy_to_db(conn,articleId,vector)
    with engine.connect() as conn:
        selectSql = """SELECT 1 FROM ArticleEmbeddings WHERE articleId = :id"""
        params = {}
        params["id"] = articleId
        rows = conn.execute(text(selectSql), params)
        assert rows.fetchone() is not None

def test_db_to_numpy():
    config = ConfigParser()
    config.read("config.ini")
    db_file = config.get('DEFAULT', 'db_file')
    engine = create_engine(db_file)
    articleId = -1    
    vector = db_to_numpy(engine,-1)
    assert vector is not None
    assert isinstance(vector, np.ndarray)
    assert vector.shape == (100,)