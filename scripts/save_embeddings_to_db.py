import os
import sys
module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)
import argparse
from pathlib import Path
import numpy as np
from tqdm import tqdm
from configparser import ConfigParser
from sqlalchemy import create_engine
from text_utils.helpers import numpy_to_db

parser = argparse.ArgumentParser()


parser.add_argument("embeddings_dir", help="Embeddings Directory that holds the .npy files")

args = parser.parse_args()
# deserialize numpy array

def deserialize_numpy_array(file_name:Path) -> tuple[np.ndarray,int, int]:
    vector = np.frombuffer(file_name.read_bytes())
    article_id = file_name.stem.split("_")[0]
    token_size = file_name.stem.split("_")[1]
    return vector,int(article_id), int(token_size)

def main():
    config = ConfigParser()
    config.read('config.ini')
    sqlalchemy_conn_string = config.get(section='DEFAULT', option='db_file')
    engine = create_engine(sqlalchemy_conn_string)
    embeddings_dir = Path(args.embeddings_dir)
    if not embeddings_dir.exists():
        print(f"Embeddings directory {embeddings_dir} must exist.")
        raise SystemExit(1)
    if not embeddings_dir.is_dir():
        print(f"Embeddings directory {embeddings_dir} must be a directory")
        raise SystemExit(1)
   
    npy_files:list[Path] 
    npy_files = [f for f in embeddings_dir.glob("*.npy") ]
    with engine.connect() as conn:
        for npy_file in tqdm(npy_files):
            vector, article_id, token_size= deserialize_numpy_array(npy_file)
            numpy_to_db(conn,article_id,vector, token_size=token_size)
        
        conn.commit()
main()
