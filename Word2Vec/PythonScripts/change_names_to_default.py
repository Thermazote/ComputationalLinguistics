import os
import sqlite3

import Patterns.persons_names_forms as person
import Patterns.attractions_names_forms as attraction

from typing import List

from pprint import pprint

from __init__ import ROOT_DIR
from config import DB_PATH

sg_persons = [
    person.bocharov, person.pisemskaya, person.ivanov, person.savchenko, person.bikadorova, person.likhachev,
    person.rusaev, person.zemtsov, person.afanasova, person.cherepakhin, person.sharifov, person.dorzhdeev,
    person.mogilniy, person.sakharova, person.sudarev, person.potapova, person.bakhin, person.merzhoeva, person.savina,
    person.nikolaev
]

vlg_attractions = [
    attraction.art_museum, attraction.exhibition_hall_of_the_museum_of_fine_arts, attraction.kazan_cathedral,
    attraction.regional_philharmonic, attraction.avant_garde, attraction.scientific_library,
    attraction.scientific_library, attraction.square_of_the_fallen_fighters, attraction.monument_to_sasha_filipov,
    attraction.museum_of_the_history_of_the_kirov_region, attraction.monument_to_the_chekists,
    attraction.armenian_church_of_st_george, attraction.monument_tram, attraction.military_train,
    attraction.gergardts_mill, attraction.dzerzhinsky_monument, attraction.tsaritsyn_fire_brigade_building,
    attraction.pavlovs_house, attraction.chelyabinsk_collective_farmer, attraction.bk_13, attraction.beit_david,
    attraction.barmaley, attraction.bald_mountain, attraction.elevator, attraction.panikha_monument,
    attraction.fountain_of_lovers, attraction.lukonins_apartment_museum,
    attraction.museum_and_exhibition_center_of_the_krasnoarmeysky_district, attraction.mamayev_kurgan,
    attraction.river_port, attraction.tsaritsyn_opera, attraction.health_history_museum,
    attraction.museum_children_of_tsaritsyn_stalingrad_volgograd,
    attraction.peoples_museum_of_volgograd_railway_workers, attraction.aviation_museum,
    attraction.tsaritsyn_stalingrad_volgograd_military_patriotic_museum_of_the_history_of_communications_and_radio_amateurism,
    attraction.park_named_after_yuri_gagarin, attraction.museum_of_the_history_of_the_volga_don_shipping_channel,
    attraction.exhibition_hall_of_the_volgograd_regional_organization_of_the_union_of_artists_of_russia,
    attraction.victory_park, attraction.komsomol_garden, attraction.childrens_city_park,
    attraction.sasha_filippov_square, attraction.friendship_park, attraction.hall_of_military_glory,
    attraction.botanical_garden_vgspu, attraction.tspkio, attraction.museum_of_musical_instruments,
    attraction.museum_of_weights_and_measures, attraction.regional_museum_of_local_lore,
    attraction.museum_reserve_old_sarepta, attraction.planetarium, attraction.museum_memory,
    attraction.museum_panorama_battle_of_stalingrad, attraction.memorial_history_museum, attraction.city_garden,
    attraction.volgograd_arena
]

DEFAULT_FORM_OF_NAME = 0


def parse_text_with_facts(article_text: List[str]) -> List[str]:
    strings_with_facts = []

    for i in range(len(article_text) - 2):
        if article_text[i].find('}') == -1 and article_text[i + 2].find('{') != -1:
            strings_with_facts.append(article_text[i])

    return strings_with_facts


def change_names_to_default(text: str) -> str:
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

    for vlg_attraction in vlg_attractions:
        for form_of_name in vlg_attraction[1:]:
            if text.find(form_of_name) != -1:
                text = text.replace(form_of_name, vlg_attraction[DEFAULT_FORM_OF_NAME])

    return text


def main():
    dbPath = DB_PATH
    db = sqlite3.connect(dbPath)
    cursor = db.cursor()

    for row in cursor.execute('SELECT id, text FROM articles ORDER BY id'):
        id, text = row

        with open(f'{ROOT_DIR}/../tomita_parser/input.txt', mode='w') as tomita_input_file:
            tomita_input_file.write(change_names_to_default(text.lower()))

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


def test():
    text = 'бочаров потаповой губернатор андрей бочаров за бочаровым андреем вместе со своим помощником дорждеевым ' \
           'отправились к шарифову руслану за консультацией насчет писемской анны, которая живет неподалеку от ' \
           'виктории афанасовой. николаев олег прибыл на место вместе со своим помощником савиной, которая ' \
           'распорядилась бахину убрать мусор алёне потаповой вместе с натальей сахаровой, где бочаров андрей был ' \
           'только за, хотя и бочаров был против андрея бочарова, который поддерживался идеями о бочарове андрее. ' \
           'несмотря на то, что волгоград арена закрылась на ремонт, в музее истории здравоохранения все еще царит ' \
           'царицынская опера, хотя не видать поблизости музея авиации. особенно я был доволен музеем "дети царицына, ' \
           'сталинграда, волгограда", ведь там парка дружбы не видать, хотя о ботаническом саде вгспу можно только и ' \
           'мечтать.'

    processed_text = change_names_to_default(text)
    pprint(processed_text)


if __name__ == '__main__':
    main()
