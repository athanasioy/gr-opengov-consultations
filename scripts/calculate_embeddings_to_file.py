import sys
import os
module_path = os.path.abspath(os.path.join("."))
if module_path not in sys.path:
    sys.path.append(module_path)

import pandas as pd
import numpy as np
from pathlib import Path
import argparse
from text_utils.textEmbeddings import GreekLongFormerEncoder

parser = argparse.ArgumentParser()

parser.add_argument("csv_file", help="Relative Path of the csv file. The CSV File must contain Id and Text as Columns")
parser.add_argument("output_dir",help= "Output directory of text embeddings.")
parser.add_argument("-t", "--test", action="store_true")
parser.add_argument("-b", "--batch_size", default=4, type=int)

args = parser.parse_args()

# Validate input
csv_file_path = Path.cwd() / Path(args.csv_file)
output_dir_path = Path.cwd() / Path(args.output_dir)
test_mode = args.test
batch_size = args.batch_size
if test_mode:
    print(f"test mode: {test_mode}")
    print(f"batch_size: {batch_size}")

if not csv_file_path.is_file():
    print(f"csv file on path {csv_file_path} does not exist!")
    raise SystemExit(2)

if not output_dir_path.is_dir() and output_dir_path.exists():
    print(f"output directory path must be a directory")
    raise SystemExit(2)

if not output_dir_path.exists():
    output_dir_path.mkdir()

encoder = GreekLongFormerEncoder()

df = pd.read_csv(csv_file_path,sep=';')

df.dropna(inplace=True)

BATCH_SIZE = batch_size
ids = df['articleId'].astype(int).tolist()
texts = df['text'].tolist()

while len(texts)>0:
  texts_batch = texts[:BATCH_SIZE]
  ids_batch = ids[:BATCH_SIZE]
  embeddings, token_sizes = encoder.get_embeddings_batch(texts_batch)

  for embedding,token_size,id in zip(embeddings,token_sizes, ids_batch):
    np.save(output_dir_path / f"{id}_{token_size}.npy", embedding)

  del texts[:BATCH_SIZE]
  del ids[:BATCH_SIZE]
  if test_mode:
      break
