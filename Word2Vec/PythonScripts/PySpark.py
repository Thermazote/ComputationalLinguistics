from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.feature import IDF
from pyspark.ml.feature import Word2Vec
from __init__ import ROOT_DIR
from pprint import pprint


def main():
    spark = SparkSession\
        .builder\
        .appName('SimpleApplication')\
        .getOrCreate()

    # Построчная загрузка файла в RDD
    # input_file = spark.sparkContext.textFile(f'{ROOT_DIR}/TextExamples/FirstExample.txt')
    # input_file = spark.sparkContext.textFile(f'{ROOT_DIR}/TextExamples/OnlyFactsText.txt')
    input_file = spark.sparkContext.wholeTextFiles(f'{ROOT_DIR}/Articles/Processed/*.txt')

    print(input_file.collect())
    prepared = input_file.map(lambda x: ([x[1]]))
    df = prepared.toDF()
    prepared_df = df.selectExpr('_1 as text')

    # Разбить на токены
    tokenizer = Tokenizer(inputCol='text', outputCol='words')
    words = tokenizer.transform(prepared_df)

    # Удалить стоп-слова
    stop_words = StopWordsRemover.loadDefaultStopWords('russian')
    remover = StopWordsRemover(inputCol='words', outputCol='filtered', stopWords=stop_words)
    filtered = remover.transform(words)

    # Вывести стоп-слова для русского языка
    print(stop_words)

    # Вывести таблицу filtered
    filtered.show()

    # Вывести столбец таблицы words с токенами до удаления стоп-слов
    words.select('words').show(truncate=False, vertical=True)

    # Вывести столбец "filtered" таблицы filtered с токенами после удаления стоп-слов
    filtered.select('filtered').show(truncate=False, vertical=True)

    # Посчитать значения TF
    vectorizer = CountVectorizer(inputCol='filtered', outputCol='raw_features').fit(filtered)
    featurized_data = vectorizer.transform(filtered)
    featurized_data.cache()
    vocabulary = vectorizer.vocabulary

    # Вывести таблицу со значениями частоты встречаемости термов.
    featurized_data.show()

    # Вывести столбец "raw_features" таблицы featurized_data
    featurized_data.select('raw_features').show(truncate=False, vertical=True)

    # Вывести список термов в словаре
    print(vocabulary)


    # Посчитать значения DF
    idf = IDF(inputCol='raw_features', outputCol='features')
    idf_model = idf.fit(featurized_data)
    rescaled_data = idf_model.transform(featurized_data)

    # Вывести таблицу rescaled_data
    rescaled_data.show()

    # Вывести столбец "features" таблицы featurized_data
    rescaled_data.select('features').show(truncate=False, vertical=True)

    # Построить модель Word2Vec
    word2Vec = Word2Vec(vectorSize=3, minCount=0, inputCol='filtered', outputCol='result')
    model = word2Vec.fit(filtered)
    w2v_df = model.transform(filtered)
    w2v_df.show()

    vocabulary = vectorizer.vocabulary
    pprint(f'Словарь:\n{vocabulary}')

    word_from_vocabulary = input('Введите одно слово из этого словаря: ').lower().strip()

    if word_from_vocabulary in vocabulary:
        print(model.findSynonyms(f'{word_from_vocabulary}', 15).collect())
    else:
        raise ValueError('Словарь не содержит данного слова!')

    spark.stop()


if __name__ == '__main__':
    main()
