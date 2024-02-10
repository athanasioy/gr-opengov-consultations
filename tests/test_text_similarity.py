import os
import sys
module_path = os.path.abspath(os.path.join(".."))
if module_path not in sys.path:
    sys.path.append(module_path)
from configparser import ConfigParser
from sqlalchemy import create_engine, text
import pytest
import numpy as np
from text_utils.textSimilarity import JaccardSimilarity, FetchFromDBVectorizer

@pytest.mark.parametrize("s1, s2, result",[
    ("test sentence","test", 1/2),
    (None,"another sentence.", 0),
    (None,None,0),
    ("Some sentence.","Should not match",0),
    ("One Third match", "One Third", 2/3),
    (""," ",0),
    ("","should not match",0)
])
def test_JaccardSimilarity(s1,s2,result):
    assert JaccardSimilarity.calculate_similarity(s1,s2) == result


def test_FetchFromDBVectorizer():
    config =ConfigParser()
    config.read('config.ini')
    sql_conn_string = config.get(section='DEFAULT', option='db_file')
    vec = FetchFromDBVectorizer(sql_conn_string,table_name="ArticleAnalysis")
    engine = create_engine(sql_conn_string)

    with engine.connect() as conn:
        sql = "Select text from Article where id = :id"
        params = {}
        params["id"] = 1000
        txt =conn.execute(text(sql), params).scalar_one()
    embedding = vec.vectorize(txt)
    assert isinstance(embedding, np.ndarray)
    assert embedding.shape == (400,)