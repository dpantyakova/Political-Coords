"""
Аналитическое приложение "Политические координаты"

Это приложение предоставляет аналитические инструменты для работы с
данными о политических координатах. Оно позволяет просматривать базу
данных, строить графики, выполнять статистические отчёты и настраивать
параметры программы.

В этом модуле содержатся функции, классы и методы, необходимые
для функционирования scripts.py

read_config(): Читает конфигурационный файл и возвращает его
содержимое в виде словаря.

read_csv(): Читает csv-файл и возвращает его содержимое в виде DataFrame.

delete_row(df, row_index): Удаляет строку из DataFrame по индексу,
перенумеровывает индексы и сохраняет изменения в csv-файл.

save_to_file(df): Сохраняет DataFrame в csv-файл.

pivot(data, values, column, index, aggfunc): Создает и выводит сводную
таблицу из DataFrame на основе указанных аргументов.

qual_var_text_report(df, qualitative_var): Создает текстовый отчет для
качественной переменной из переданного DataFrame.

quantitive_text_report(df, quantitative_vars): Создает текстовый отчет
для количественных переменных из переданного DataFrame.
"""
import pandas as pd
import json
import os


def read_config():
    """
    Читает конфигурационный файл и возвращает его содержимое в виде словаря.

    Возвращает:
        dict: Содержимое конфигурационного файла.
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'scripts',
                               'config.json')
    with open(config_path, 'r', encoding="utf-8") as config_file:
        config = json.load(config_file)
    return config


def read_csv():
    """
    Читает csv-файл и возвращает его содержимое в виде DataFrame.

    Возвращает:
        pd.DataFrame: Содержимое csv-файла.
    """
    config = read_config()
    data = pd.read_csv(config["db"]["csv"], encoding='utf-8')
    return data


data = read_csv()


def delete_row(df, row_index):
    """
    Удаляет строку из DataFrame по индексу, перенумеровывает индексы и
    сохраняет изменения в csv-файл.

    Аргументы:
        df (pd.DataFrame): Исходный DataFrame, из которого нужно удалить
        строку.
        row_index (int): Индекс строки, которую нужно удалить.

    Возвращает:
        pd.DataFrame: DataFrame с обновленным содержимым.
    """
    df = df.drop(row_index)
    df = df.reset_index(drop=True)
    df['id'] = range(1, len(df) + 1)
    save_to_file(df)
    data = read_csv()
    return data


def save_to_file(df):
    """
    Сохраняет DataFrame в csv-файл.

    Аргументы:
        df (pd.DataFrame): DataFrame, который нужно сохранить в csv-файл.
    """
    config = read_config()
    df.to_csv(config["db"]["csv"], index=False)


def pivot(data, values, column, index, aggfunc):
    """
    Создает и выводит сводную таблицу из DataFrame на основе указанных
    аргументов.

    Если указанный столбец не найден в DataFrame, выводит соответствующее
    сообщение.

    Аргументы:
        data (pd.DataFrame): Исходный DataFrame, из которого будет создана
        сводная таблица.
        values (str): Имя столбца, который используется для вычисления
        агрегированных значений.
        column (str): Имя столбца, который будет использоваться для создания
        столбцов в сводной таблице.
        index (str): Имя столбца, который будет использоваться для создания
        индекса в сводной таблице.
        aggfunc (function): Функция, которую нужно применить к значениям в
        сводной таблице.

    Возвращает:
        pd.DataFrame: Сводная таблица, созданная из исходного DataFrame.
                      Если указанный столбец не найден, возвращает None.
    """
    if column in data.columns:
        # создание сводной таблицы
        pivot_table = pd.pivot_table(data, values=values, index=index,
                                     columns=column, aggfunc=aggfunc)

        # вывод заголовка отчета и сводной таблицы
        return pivot_table
    print("Столбец не найден в DataFrame")


def qual_var_text_report(df, qualitative_var):
    """
    Создает текстовый отчет для качественной переменной из переданного
    DataFrame.

    Параметры:
    df (pandas.DataFrame): DataFrame, который содержит качественную переменную.
    qualitative_var (str): Имя столбца в df, который представляет качественную
    переменную.

    Возвращает:
    table (pandas.DataFrame): DataFrame, который содержит три столбца -
    'Значение', 'Частоты' и 'Процент'.
    Частоты показывают, сколько раз каждое уникальное значение встречается
    в данных,
    Процент показывает процентное соотношение, которое каждое уникальное
    значение составляет от общего числа.
    """
    if qualitative_var in df.columns:
        counts = df[qualitative_var].value_counts()
        percentages = df[qualitative_var].value_counts(normalize=True) * 100
        table = pd.DataFrame({
            'Значение': counts.index,
            'Частоты': counts.values,
            'Процент': percentages.values
        })
        return table
    else:
        return pd.DataFrame()
    # Возвращает пустой DataFrame, если заданной колонки не существует


def quantitive_text_report(df, quantitative_vars):
    """
    Создает текстовый отчет для количественных переменных из переданного
    DataFrame.

    Параметры:
    df (pandas.DataFrame): DataFrame, который содержит количественные
    переменные.
    quantitative_vars (list): Список имен столбцов в df, которые представляют
    количественные переменные.

    Возвращает:
    table (pandas.DataFrame): DataFrame, который содержит статистические меры
    (минимум, максимум, среднее,
    стандартное отклонение и т.д.) для каждой из количественных переменных.

    Использует метод describe() для создания отчета.
    """
    table = df[quantitative_vars].describe()
    return table
