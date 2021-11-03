import os
import sqlite3

import Patterns.end_of_persons_names_forms as person

from typing import List

from pprint import pprint
from __init__ import ROOT_DIR


sg_persons = [person.bocharov, person.pisemskaya, person.ivanov, person.savchenko, person.bikadorova,
              person.likhachev, person.rusaev, person.zemtsov, person.afanasova, person.cherepakhin,
              person.sharifov, person.dorzhdeev, person.mogilniy, person.sakharova, person.sudarev,
              person.potapova, person.bakhin, person.merzhoeva, person.savina, person.nikolaev]

DEFAULT_FORM_OF_NAME = 0


def parse_text_with_facts(article_text: List[str]) -> List[str]:
    strings_with_facts = []

    for i in range(len(article_text) - 2):
        if article_text[i].find('}') == -1 and article_text[i + 2].find('{') != -1:
            strings_with_facts.append(article_text[i])

    return strings_with_facts


def change_person_names_to_default(text: str) -> str:
    for sg_person in sg_persons:
        for form_of_name in sg_person[1:]:
            if text.find(form_of_name) != -1:
                if form_of_name.find(' ') != -1:
                    text = text.replace(form_of_name, sg_person[DEFAULT_FORM_OF_NAME])
                else:
                    try:
                        if text.index(form_of_name) == 0:
                            text = text.replace(form_of_name, sg_person[DEFAULT_FORM_OF_NAME], 1)
                    finally:
                        text = text.replace(f' {form_of_name}', f' {sg_person[DEFAULT_FORM_OF_NAME]}')

    return text


def main():
    dbPath = f'{ROOT_DIR}/../web_parser/db.sqlite'
    db = sqlite3.connect(dbPath)
    cursor = db.cursor()

    for row in cursor.execute('SELECT id, text FROM articles ORDER BY id'):
        id, text = row

        with open(f'{ROOT_DIR}/../tomita_parser/input.txt', mode='w') as tomita_input_file:
            tomita_input_file.write(change_person_names_to_default(text.lower()))

        os.system('cd ../../tomita_parser/ && ./tomita-parser config.proto')

        with open(f'{ROOT_DIR}/../tomita_parser/output.txt', mode='r') as tomita_output_file:
            article_text = tomita_output_file.readlines()

            with open(f'{ROOT_DIR}/Articles/AfterTomita/article_{id}.txt', mode='w') as tomita_article:
                tomita_article.writelines(article_text)

            processed_article_text = parse_text_with_facts(article_text)

            if processed_article_text:
                with open(f'{ROOT_DIR}/Articles/Processed/article_{id}.txt', mode='w') as proccessed_output_file:
                    proccessed_output_file.writelines(processed_article_text)

                only_facts_article_text = ' '.join(processed_article_text)

                aDataSet = (only_facts_article_text, id)
                cursor.execute('INSERT INTO articles_facts(text, article_id) VALUES(?,?)', aDataSet)
                db.commit()


if __name__ == '__main__':
    main()
