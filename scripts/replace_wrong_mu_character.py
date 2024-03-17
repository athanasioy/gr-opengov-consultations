import os
import sys
module_path = os.path.abspath(os.path.join('.'))

if module_path not in sys.path:
    sys.path.append(module_path)


from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import tqdm
from data_objects.article import Article
from text_utils.textDecorators import ReplaceWrongGreekMuCharacterDecorator

def main():
    db = "sqlite:///opengov.db"
    engine = create_engine(db)

    dec = ReplaceWrongGreekMuCharacterDecorator(None)

    with Session(engine) as sess:
        stmt = select(Article)
        articles = sess.execute(stmt).scalars()

        for article in tqdm.tqdm(articles):
            article.text = dec.execute(article.text)
        
        sess.commit()


main()