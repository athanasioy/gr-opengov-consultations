import os
import sys
module_path = os.path.abspath(os.path.join('.'))

if module_path not in sys.path:
    sys.path.append(module_path)


from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from bs4 import BeautifulSoup
import tqdm
import requests

from data_objects.legislation import Legislation
from text_utils.textDecorators import ReplaceWrongGreekMuCharacterDecorator

def get_correct_title(url:str) -> str:
    r=requests.get(url)
    soup = BeautifulSoup(r.content, features="html.parser")
    titles = soup.select('h3')
    title = titles[len(titles)-1].text
    return title

def main():
    db = "sqlite:///opengov.db"
    engine = create_engine(db)

    with Session(engine) as sess:
        stmt = select(Legislation).where(Legislation.is_public_consultation==1)
        public_consultations = sess.execute(stmt).scalars()

        for legObj in tqdm.tqdm(public_consultations):
            print(f"{legObj}")
            correct_title = get_correct_title(legObj.scrap_url)
            legObj.title = correct_title
            print(legObj)
            # break
        
        sess.commit()

main()