# comp_linguistics
## Develop
### ToDo List
#### Thermazote (Резников Никита ИВТ-360)
Распарсить сайт из списка и вывести в web-интерфейсе данные согласно номеру задания. Краулер должен считывать новостную ленту с первой страницы сайта. Периодичность повторения устанавливается пользователем. Данные заполняются в БД MongoDB. Обязательные поля для текста новости:
- Название новости
- Дата новости
- Ссылка на новость
- Текст новости
- Ссылка на видео (если есть)
- Количество просмотров новости (если есть)
- Количество комментариев новости (если есть)
При учередном проходе краулера для существующих в БД новостей (определяется по -Название новости, Дата новости, Ссылка на новость) поля количества просмотров и комментариев обновляются.
#### MrKobrand (Рублёв Александр ИВТ-363)
Создать программный модкль для анализа новостей из БД. Выделить с помощью Томита-парсера упоминание в тексте значимых персон Волгоградской области и достопримечательностей. Зафиксировать в БД предложения с их упоминанием для дальнейшего анализа тональности.
Создать программный модуль для проведения с помощью Spark MlLib анализ модели word2vec на всем объеме новостных статей из БД. Для персон Волгоградской области и достопримечательностей определить контектные синонимы и слова, с которыми они упоминались в тексте.
Персоны: https://global-volgograd.ru/person
Достопримечательности: https://avolgograd.com/sights?obl=vgg
#### Ambashadur (Меркулов Владислав ИВТ-365)
Создать программный модуль для выявления тональности высказываний по отношению к персонам Волгоградской области и достопримечательностям.
Можно использовать либо подход на основе правил и словарей, либо методы машинного обучения.
