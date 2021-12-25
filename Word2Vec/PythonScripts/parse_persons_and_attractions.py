import os
import pymongo

import Patterns.persons_names_forms as person
import Patterns.attractions_names_forms as attraction

from typing import List
from datetime import datetime, timedelta
from pprint import pprint

from __init__ import ROOT_DIR
from config import MONGO_USERNAME, MONGO_PASSWORD

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


def change_attraction_names_to_default(text: str) -> str:
    for vlg_attraction in vlg_attractions:
        for form_of_name in vlg_attraction[1:]:
            if text.find(form_of_name) != -1:
                text = text.replace(form_of_name, vlg_attraction[DEFAULT_FORM_OF_NAME])

    return text


def main():
    CONN_STR = f'mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.8ngl3.mongodb.net'
    client = pymongo.MongoClient(CONN_STR, serverSelectionTimeoutMS=5000)
    db = client['articles_analysis']
    articles_coll = db['articles']

    # for document in articles_coll.find({'facts': {'$exists': True}}):
    #     articles_coll.update_one({'_id': document['_id']}, {'$unset': {'facts': 1}})

    # for document in articles_coll.find():
    #     print(document['date'])
    #     date_time_obj = datetime.strptime(document['date'], '%d.%m.%Y %H:%M')
    #     print(date_time_obj - timedelta(hours=1), date_time_obj)
    #     print(date_time_obj - timedelta(hours=1) < date_time_obj)
    #     break

    # i = 0
    # for document in articles_coll.find():
    #     i += 1
    #     with open(f'{ROOT_DIR}/Articles/ArticlesTextNew/article_{i}.txt', mode='w') as article_text_file:
    #         article_text_file.write(document['text'])

    for document in articles_coll.find({'facts': {'$exists': False}}):
        print(document['_id'])

        changed_text = change_person_names_to_default(document['text'])  # text.lower()

        with open(f'{ROOT_DIR}/../tomita_parser/input.txt', mode='w') as tomita_input_file:
            tomita_input_file.write(changed_text)

        os.system('cd ../../tomita_parser/ && ./tomita-parser config.proto')

        with open(f'{ROOT_DIR}/../tomita_parser/output.txt', mode='r') as tomita_output_file:
            article_text = tomita_output_file.readlines()

        processed_article_text = parse_text_with_facts(article_text)

        if processed_article_text:
            # Processing after tomita
            only_facts_article_text = change_attraction_names_to_default(' '.join(processed_article_text).lower())
            articles_coll.update_one({'_id': document['_id']}, {'$set': {'facts': only_facts_article_text}})
            print(f'{only_facts_article_text}\n-----------------------------')


def test():
    text = 'Бочаров Потаповой Губернатор Андрей Бочаров За Бочаровым Андреем Вместе Со Своим Помощником Дорждеевым ' \
           'отправились К Шарифову Руслану За Консультацией Насчет Писемской Анны, Которая Живет Неподалеку От ' \
           'Виктории Афанасовой. Николаев Олег Прибыл На Место Вместе Со Своим Помощником Савиной, Которая ' \
           'распорядилась Бахину Убрать Мусор Алёне Потаповой Вместе С Натальей Сахаровой, Где Бочаров Андрей Был ' \
           'только За, Хотя И Бочаров Был Против Андрея Бочарова, Который Поддерживался Идеями О Бочарове Андрее. ' \
           'несмотря На То, Что Волгоград Арена Закрылась На Ремонт, В Музее Истории Здравоохранения Все Еще Царит ' \
           'царицынская Опера, Хотя Не Видать Поблизости Музея Авиации. Особенно Я Был Доволен Музеем "дети Царицына, ' \
           'сталинграда, Волгограда", Ведь Там Парка Дружбы Не Видать, Хотя О Ботаническом Саде Вгспу Можно Только И ' \
           'мечтать.'

    processed_text = change_person_names_to_default(text)
    pprint(processed_text)


if __name__ == '__main__':
    # test()
    main()
