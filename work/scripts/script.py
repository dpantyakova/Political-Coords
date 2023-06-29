"""
Аналитическое приложение "Политические координаты"

Это приложение предоставляет аналитические инструменты для работы с данными о
политических координатах. Оно позволяет просматривать базу данных, строить
графики, выполнять статистические отчёты и настраивать параметры программы.

В этом модуле содержатся функции, классы и методы, необходимые для
функционирования приложения

классы
GUI - Класс для создания графического интерфейса приложения "Политические
координаты"

методы
create_widgets - Метод для создания виджетов на главном окне приложения
plot_data - Метод для построения графика на основе переданных данных
change_theme - Метод для изменения темы оформления приложения
save_plot - Метод для сохранения построенного графика в файл
quit_app - Метод для завершения работы приложения
create_widgets - Метод для создания виджетов на главном окне приложения.
Создает вкладки и фреймы, устанавливает стили.

Функции
__init__ - Инициализирует графическое приложение 'Политические координаты'.
set_styles - Настраивает стили виджетов для приложения.
delete_update - Удаляет строку с заданным индексом из таблицы и обновляет
таблицу.
save_settings - Сохраняет настройки, введенные пользователем.
next_question - Переходит к следующему вопросу в тесте и обновляет результаты
ответов.
create_report_from_dataframe - Создает отчет из данных DataFrame и отображает
его в виджете Treeview.
bar - Функция создает кластеризованную столбчатую диаграмму (bar plot) с
использованием библиотеки matplotlib.pyplot.
plot_hist - Функция создает гистограмму для пары "количественный атрибут -
качественный атрибут" с использованием библиотеки matplotlib.
reate_boxplot - Функция создает ящиковую диаграмму (boxplot) для пары
"количественный атрибут - качественный атрибут" с использованием библиотеки
matplotlib.pyplot.
"""

import os
import random
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import ttk
import tkinter as tk
import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.getcwd(), '..'))

os.chdir(".")
from work.library.library import *

config_path = os.path.join(os.path.dirname(
    __file__), '..', 'scripts', 'config.json')

config = read_config()


class GUI(tk.Tk):
    """
    Класс для создания графического интерфейса приложения "Политические 
    координаты"
    """

    def __init__(self):
        """
        Инициализирует графическое приложение 'Политические координаты'.

        Метод __init__ настраивает начальную конфигурацию окна приложения.
        Он устанавливает заголовок окна, тему и позицию, а также запрещает 
        изменение размеров окна.
        Затем вызывается метод create_widgets для создания необходимых 
        виджетов для приложения.

        Аргументы:
            Нет

        Возвращает:
            Нет
        """
        super().__init__()

        self.title("Аналитическое приложение 'Политические координаты'")
        self.theme = config["theme_now"]

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Рассчитываем координаты окна для размещения его в центре экрана
        x = (screen_width - int(config[self.theme]["WINDOW_WIDTH"])) // 2
        y = (screen_height - int(config[self.theme]["WINDOW_HEIGHT"])) // 2

        width = int(config[self.theme]["WINDOW_WIDTH"])
        height = int(config[self.theme]["WINDOW_HEIGHT"])
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(width=False, height=False)

        self.create_widgets()

    def create_widgets(self):
        """
        Метод для создания виджетов на главном окне приложения

        Создает вкладки и фреймы, устанавливает стили.

        """
        # Установка стилей
        self.set_styles()

        # Создание вкладок и фреймов
        notebook = ttk.Notebook(self, style='lefttab.TNotebook')
        notebook.pack(fill='y', side='left')

        f1 = ttk.Frame(notebook, style='main.TFrame',
                       width=config[self.theme]["FRAME_WIDTH"],
                       height=config[self.theme]["FRAME_HEIGHT"])
        f2 = ttk.Frame(notebook, style='main.TFrame',
                       width=config[self.theme]["FRAME_WIDTH"],
                       height=config[self.theme]["FRAME_HEIGHT"])
        f3 = ttk.Frame(notebook, style='main.TFrame',
                       width=config[self.theme]["FRAME_WIDTH"],
                       height=config[self.theme]["FRAME_HEIGHT"])
        f4 = ttk.Frame(notebook, style='main.TFrame',
                       width=config[self.theme]["FRAME_WIDTH"],
                       height=config[self.theme]["FRAME_HEIGHT"])
        f5 = ttk.Frame(notebook, style='main.TFrame',
                       width=config[self.theme]["FRAME_WIDTH"],
                       height=config[self.theme]["FRAME_HEIGHT"])
        f6 = ttk.Frame(notebook, style='main.TFrame',
                       width=config[self.theme]["FRAME_WIDTH"],
                       height=config[self.theme]["FRAME_HEIGHT"])
        f7 = ttk.Frame(notebook, style='main.TFrame',
                       width=config[self.theme]["FRAME_WIDTH"],
                       height=config[self.theme]["FRAME_HEIGHT"])
        f8 = ttk.Frame(notebook, style='main.TFrame',
                       width=config[self.theme]["FRAME_WIDTH"],
                       height=config[self.theme]["FRAME_HEIGHT"])
        f9 = ttk.Frame(notebook, style='main.TFrame',
                       width=config[self.theme]["FRAME_WIDTH"],
                       height=config[self.theme]["FRAME_HEIGHT"])

        notebook.add(f1, text='Работа с БД')
        notebook.add(f2, text='Статистический отчёт')
        notebook.add(f3, text='Сводная таблица')
        notebook.add(f4, text='Кластеризованная столбчатая диаграмма')
        notebook.add(f5, text='Категоризированная гистограмма')
        notebook.add(f6, text='Категоризированная диаграмма Бокса-Вискера')
        notebook.add(f7, text='Категоризированная диаграмма рассеивания')
        notebook.add(f8, text='Пройти тест!')
        notebook.add(f9, text='Настройки программы')

        # Создание виджетов для вкладки Работа с БД
        f1_info_label = ttk.Label(f1,
                                  text="Инструмент позволяет просмотреть" +
                                       " базу данных и удалить записи в ней." +
                                       " В таблице работает пролистывание." +
                                       "\nОсь х показывает тип экономики, " +
                                       "который больше всего симпотизирует " +
                                       "\nреспонденту (положительные значения " +
                                       "- рыночная, отрицательные - плановая" +
                                       "),\n ось у - ось авторитаризма (верх)" +
                                       " / либерализм, ось" +
                                       "z - ось прогрессивности (более " +
                                       "\nположительные значения - больше " +
                                       "прогрессивности).",
                                  style='main.TLabel')

        f1_output_text = ttk.Treeview(f1)
        f1_output_text["show"] = "headings"

        self.create_report_from_dataframe(data, f1_output_text)

        for column in f1_output_text["columns"]:
            f1_output_text.column(column, width=int(
                config[self.theme]["FRAME_WIDTH"] / 10))

        f1_del_label = ttk.Label(f1,
                                 text="Выберите запись для удаления: ",
                                 style='main.TLabel')

        f1_record_to_del_var = tk.StringVar()
        f1_record_to_del_entry = tk.Entry(f1,
                                          textvariable=f1_record_to_del_var,
                                          bg=config[self.theme]["ACCENT_COLOR_LIGHT"],
                                          width=50)

        f1_del_button = ttk.Button(f1, text="Удалить",
                                   command=lambda: self.delete_update(
                                       f1_record_to_del_var.get(),
                                       f1_output_text, f1),
                                   style='main.TButton')

        f1_info_label.grid(row=0, column=0, columnspan=3, sticky="w")
        f1_output_text.grid(row=1, column=0, columnspan=3)
        f1_del_label.grid(row=2, column=0, sticky="w")
        f1_record_to_del_entry.grid(row=2, column=0, padx=10, sticky="e")
        f1_del_button.grid(row=3, column=0, pady=10, sticky="e")

        # Создание виджетов для вкладки "Статистический отчёт"
        f2_info_label = ttk.Label(f2,
                                  text="Этот инструмент позволяет создать " +
                                       "категоризированную гистограмму для пары " +
                                       "качественный - количественный атрибут",
                                  style='main.TLabel')
        f2_first_attribute = tk.StringVar()
        f2_first_attribute_label = ttk.Label(
            f2, text="Качественный атрибут:", style='main.TLabel')

        f2_first_attribute_cb = ttk.Combobox(
            f2, textvariable=f2_first_attribute, style='main.TCombobox')
        f2_first_attribute_cb['values'] = [
            "gender", "field", "university", "course"]

        f2_second_attribute = tk.StringVar()
        f2_second_attribute_label = ttk.Label(
            f2, text="Количественный атрибут:", style='main.TLabel')

        f2_second_attribute_cb = ttk.Combobox(
            f2, textvariable=f2_second_attribute, style='main.TCombobox')
        f2_second_attribute_cb['values'] = ["x", "y", "z"]

        f2_output_text = ttk.Treeview(f2)
        # чтобы скрыть пустую колонку
        f2_output_text["show"] = "headings"

        f2_create_button1 = ttk.Button(f2, text="Создать отчет для " +
                                                "качественного атрибута",
                                       command=lambda:
                                       self.create_report_from_dataframe(
                                           qual_var_text_report(
                                               data,
                                               f2_first_attribute.get()),
                                           f2_output_text),
                                       style='main.TButton')

        f2_create_button2 = ttk.Button(f2, text="Создать отчет для " +
                                                "количественного атрибута",
                                       command=lambda:
                                       self.create_report_from_dataframe(
                                           pd.DataFrame({
                                               'Статистика':
                                                   ['Всего',
                                                    'Среднее',
                                                    'Отклонение',
                                                    'Минимальное',
                                                    '25%',
                                                    '50%', '75%',
                                                    'Максимальное'],
                                               'Значение':
                                                   quantitive_text_report(
                                                       data,
                                                       f2_second_attribute.get()
                                                   )
                                           }),
                                           f2_output_text),
                                       style='main.TButton')

        f2_info_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        f2_first_attribute_label.grid(row=1, column=0, padx=10, pady=5)
        f2_first_attribute_cb.grid(row=1, column=1, padx=10, pady=5)

        f2_second_attribute_label.grid(row=2, column=0, padx=10, pady=5)
        f2_second_attribute_cb.grid(row=2, column=1, padx=10, pady=5)

        f2_create_button1.grid(row=3, column=0, padx=10, pady=5)
        f2_create_button2.grid(row=3, column=1, padx=10, pady=5)

        f2_output_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Создание виджетов для вкладки "Сводная таблица"
        f3_info_label = ttk.Label(f3, text="Это - текстовый отчет для пары" +
                                           " двух качественных атрибутов.",
                                  style='main.TLabel')

        f3_axis_var = tk.StringVar()
        f3_axis_label = ttk.Label(f3, text="Ось:", style='main.TLabel')

        f3_axis_cb = ttk.Combobox(
            f3, textvariable=f3_axis_var, style='main.TCombobox')
        f3_axis_cb['values'] = ["x", "y", "z"]

        f3_first_attribute = tk.StringVar()
        f3_first_attribute_label = ttk.Label(
            f3, text="Первый атрибут:", style='main.TLabel')

        f3_first_attribute_cb = ttk.Combobox(
            f3, textvariable=f3_first_attribute, style='main.TCombobox')
        f3_first_attribute_cb['values'] = [
            "gender", "field", "university", "course"]

        f3_second_attribute = tk.StringVar()
        second_attribute_label = ttk.Label(
            f3, text="Второй атрибут:", style='main.TLabel')

        f3_second_attribute_cb = ttk.Combobox(
            f3, textvariable=f3_second_attribute, style='main.TCombobox')
        f3_second_attribute_cb['values'] = [
            "gender", "field", "university", "course"]

        f3_agg_method = tk.StringVar()
        f3_agg_method_label = ttk.Label(
            f3, text="Метод агрегации:", style='main.TLabel')

        f3_agg_method_cb = ttk.Combobox(
            f3, textvariable=f3_agg_method, style='main.TCombobox')
        f3_agg_methods = {"Сумма": "sum",
                          "Среднее значение": "mean",
                          "Минимум": "min",
                          "Максимум": "max",
                          "Медиана": "median"}
        f3_agg_method_cb['values'] = list(f3_agg_methods.keys())

        f3_pivot_create_button = ttk.Button(f3, text="Создать сводную таблицу",
                                            command=lambda:
                                            self.create_report_from_dataframe(
                                                pivot(data, f3_axis_var.get(),
                                                      f3_first_attribute.get(),
                                                      f3_second_attribute.get(),
                                                      f3_agg_methods[
                                                          f3_agg_method.get()]
                                                      ).reset_index().round(1),
                                                f3_pivot_output_text),
                                            style='main.TButton')

        f3_pivot_output_text = ttk.Treeview(f3)
        # чтобы скрыть пустую колонку
        f3_pivot_output_text["show"] = "headings"

        f3_info_label.grid(row=0, column=0, columnspan=2,
                           sticky="w", padx=5, pady=5)
        f3_axis_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        f3_axis_cb.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        f3_first_attribute_label.grid(
            row=2, column=0, sticky="w", padx=5, pady=5)
        f3_first_attribute_cb.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        second_attribute_label.grid(
            row=3, column=0, sticky="w", padx=5, pady=5)
        f3_second_attribute_cb.grid(
            row=3, column=1, sticky="w", padx=5, pady=5)
        f3_agg_method_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        f3_agg_method_cb.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        f3_pivot_create_button.grid(
            row=5, column=0, columnspan=2, padx=5, pady=5)
        f3_pivot_output_text.grid(
            row=6, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        # Создание виджетов для вкладки "Кластеризованная столбчатая диаграмма"
        f4_label1 = ttk.Label(f4, text="Первый атрибут:", style='main.TLabel')

        f4_bar_attribute1 = tk.StringVar()
        f4_combobox1 = ttk.Combobox(f4, textvariable=f4_bar_attribute1,
                                    values=["gender", "field",
                                            "university", "course"],
                                    style='main.TCombobox')

        f4_label2 = ttk.Label(f4, text="Второй атрибут:", style='main.TLabel')

        f4_bar_attribute2 = tk.StringVar()
        f4_combobox2 = ttk.Combobox(f4, textvariable=f4_bar_attribute2,
                                    values=["gender", "field",
                                            "university", "course"],
                                    style='main.TCombobox')

        f4_button = ttk.Button(f4, text="Создать диаграмму",
                               command=lambda: self.bar(f4,
                                                        data,
                                                        f4_bar_attribute1.get(),
                                                        f4_bar_attribute2.get(),
                                                        row=5,
                                                        column=0,
                                                        columnspan=2),
                               style='main.TButton')

        f4_label1.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        f4_combobox1.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        f4_label2.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        f4_combobox2.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        f4_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Создание виджетов для вкладки Категоризованная гистограмма
        f5_info_label = ttk.Label(f5,
                                  text="Этот инструмент позволяет создать" +
                                       " категоризированную гистограмму для пары" +
                                       " качественный - количественный атрибут",
                                  style='main.TLabel')
        f5_first_attribute = tk.StringVar()
        f5_first_attribute_label = ttk.Label(
            f5, text="Качественный атрибут:", style='main.TLabel')

        f5_first_attribute_cb = ttk.Combobox(
            f5, textvariable=f5_first_attribute, style='main.TCombobox')
        f5_first_attribute_cb['values'] = [
            "gender", "field", "university", "course"]

        f5_second_attribute = tk.StringVar()
        f5_second_attribute_label = ttk.Label(
            f5, text="Количественный атрибут:", style='main.TLabel')

        f5_second_attribute_cb = ttk.Combobox(
            f5, textvariable=f5_second_attribute, style='main.TCombobox')
        f5_second_attribute_cb['values'] = ["x", "y", "z"]

        f5_create_button = ttk.Button(f5, text="Создать категоризированную" +
                                               " гистограмму",
                                      command=lambda:
                                      self.plot_hist(f5,
                                                     data,
                                                     f5_first_attribute.get(), f5_second_attribute.get(),
                                                     row=4, column=0,
                                                     columnspan=2),
                                      style='main.TButton')

        f5_info_label.grid(row=0, column=0, columnspan=2)
        f5_first_attribute_label.grid(row=1, column=0)
        f5_first_attribute_cb.grid(row=1, column=1)
        f5_second_attribute_label.grid(row=2, column=0)
        f5_second_attribute_cb.grid(row=2, column=1)
        f5_create_button.grid(row=3, column=0, columnspan=2)

        # Диаграмма Бокса-Вискера
        f6_info_label = ttk.Label(f6,
                                  text="Этот инструмент позволяет создать" +
                                       " диаграмму Бокса-Вискера для пары" +
                                       " качественный - количественный атрибут",
                                  style='main.TLabel')
        f6_first_attribute = tk.StringVar()
        f6_first_attribute_label = ttk.Label(
            f6, text="Качественный атрибут:", style='main.TLabel')

        f6_first_attribute_cb = ttk.Combobox(
            f6, textvariable=f6_first_attribute, style='main.TCombobox')
        f6_first_attribute_cb['values'] = [
            "gender", "field", "university", "course"]

        f6_second_attribute = tk.StringVar()
        f6_second_attribute_label = ttk.Label(
            f6, text="Количественный атрибут:", style='main.TLabel')

        f6_second_attribute_cb = ttk.Combobox(
            f6, textvariable=f6_second_attribute, style='main.TCombobox')
        f6_second_attribute_cb['values'] = ["x", "y", "z"]

        f6_create_button = ttk.Button(f6, text="Создать диаграмму " +
                                               "Бокса-Вискера",
                                      command=lambda:
                                      self.create_boxplot(f6,
                                                          data,
                                                          f6_first_attribute.get(), f6_second_attribute.get(), row=4,
                                                          column=0,
                                                          columnspan=2),
                                      style='main.TButton')

        f6_info_label.grid(row=0, column=0, columnspan=2)
        f6_first_attribute_label.grid(row=1, column=0)
        f6_first_attribute_cb.grid(row=1, column=1)
        f6_second_attribute_label.grid(row=2, column=0)
        f6_second_attribute_cb.grid(row=2, column=1)
        f6_create_button.grid(row=3, column=0, columnspan=2)

        # Категоризированная диаграмма рассеивания
        f7_info_label = ttk.Label(f7,
                                  text="Этот инструмент позволяет" +
                                       " создать диаграмму рассеивания " +
                                       "для двух количественных атрибутов и " +
                                       "одного качественного атрибута",
                                  style='main.TLabel')
        f7_first_attribute = tk.StringVar()
        f7_first_attribute_label = ttk.Label(
            f7, text="Качественный атрибут:", style='main.TLabel')

        f7_first_attribute_cb = ttk.Combobox(
            f7, textvariable=f7_first_attribute, style='main.TCombobox')
        f7_first_attribute_cb['values'] = [
            "gender", "field", "university", "course"]

        f7_second_attribute = tk.StringVar()
        f7_second_attribute_label = ttk.Label(
            f7, text="Количественный атрибут 1:", style='main.TLabel')

        f7_second_attribute_cb = ttk.Combobox(
            f7, textvariable=f7_second_attribute, style='main.TCombobox')
        f7_second_attribute_cb['values'] = ["x", "y", "z"]

        f7_third_attribute = tk.StringVar()
        f7_third_attribute_label = ttk.Label(
            f7, text="Количественный атрибут 2:", style='main.TLabel')

        f7_third_attribute_cb = ttk.Combobox(
            f7, textvariable=f7_third_attribute, style='main.TCombobox')
        f7_third_attribute_cb['values'] = ["x", "y", "z"]

        f7_create_button = ttk.Button(f7, text="Создать диаграмму рассеивания",
                                      command=lambda:
                                      self.plot_scatter(f7,
                                                        data,
                                                        f7_first_attribute.get(), f7_second_attribute.get(),
                                                        f7_third_attribute.get(),
                                                        row=5,
                                                        column=0,
                                                        columnspan=2),
                                      style='main.TButton')

        f7_info_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        f7_first_attribute_label.grid(row=1, column=0, padx=10, pady=10)
        f7_first_attribute_cb.grid(row=1, column=1, padx=10, pady=10)

        f7_second_attribute_label.grid(row=2, column=0, padx=10, pady=10)
        f7_second_attribute_cb.grid(row=2, column=1, padx=10, pady=10)

        f7_third_attribute_label.grid(row=3, column=0, padx=10, pady=10)
        f7_third_attribute_cb.grid(row=3, column=1, padx=10, pady=10)

        f7_create_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Пройти тест
        f8_sex_var = tk.StringVar()
        f8_sex_var.set("Выберите пол")
        f8_sex_cb = ttk.Combobox(
            f8, textvariable=f8_sex_var,
            values=config["sexes"], style='main.TCombobox')

        f8_direction_var = tk.StringVar()
        f8_direction_var.set("Выберите направление подготовки")
        f8_direction_cb = ttk.Combobox(f8, textvariable=f8_direction_var,
                                       values=config["directions"],
                                       style='main.TCombobox')

        f8_university_var = tk.StringVar()
        f8_university_var.set("Выберите университет")
        f8_university_cb = ttk.Combobox(f8, textvariable=f8_university_var,
                                        values=config["universities"],
                                        style='main.TCombobox')

        f8_course_var = tk.StringVar()
        f8_course_var.set("Выберите курс обучения (бакалавриат/специалитет)")
        f8_course_cb = ttk.Combobox(f8, textvariable=f8_course_var,
                                    values=config["courses"],
                                    style='main.TCombobox')

        self.questions = config["questions"]
        random.shuffle(self.questions)
        self.current_question = 0

        f8_question_label = ttk.Label(
            f8, text=self.questions[0]["question"], style='main.TLabel')

        self.answer = tk.StringVar()
        f8_options = [ttk.Radiobutton(f8, text=option, variable=self.answer,
                                      value=option, style='main.TRadiobutton')
                      for option in list(config["options"].keys())]

        f8_next_question_button = ttk.Button(f8, text="Следующий вопрос",
                                             command=lambda:
                                             self.next_question(
                                                 self.answer.get(),
                                                 f8_question_label,
                                                 f8_sex_var.get(),
                                                 f8_direction_var.get(),
                                                 f8_university_var.get(),
                                                 f8_course_var.get()),
                                             style='main.TButton')

        self.new_answer = {
            'id': [],
            'gender': [],
            'field': [],
            'university': [],
            'course': [],
            'x': 0,
            'y': 0,
            'z': 0
        }

        f8_sex_cb.grid(row=0, column=0, sticky="w")
        f8_direction_cb.grid(row=1, column=0, sticky="w")
        f8_university_cb.grid(row=2, column=0, sticky="w")
        f8_course_cb.grid(row=3, column=0, sticky="w")
        #
        f8_question_label.grid(row=4, column=0, sticky="w")
        #
        for idx, option in enumerate(f8_options):
            option.grid(row=5 + idx, column=0, sticky="w")
        #
        f8_next_question_button.grid(row=9, column=0, sticky="w")

        # Настройки
        self.theme_choose = tk.StringVar()
        theme_choose_cb = ttk.Combobox(f9, textvariable=self.theme_choose,
                                       values=config["themes"]["themes"],
                                       style='main.TCombobox')
        self.theme_choose.set("theme1")

        path_lb = tk.Label(f9, text="Путь к базе данных:",
                           bg=config[self.theme]["BACKGROUND_COLOR"])

        self.path_db = tk.StringVar()
        self.path_db.set(config["db"]["path"])
        path_entry = tk.Entry(f9, textvariable=self.path_db,
                              bg=config[self.theme]["ACCENT_COLOR_LIGHT"],
                              width=50)

        save_settings_button = tk.Button(f9, text="Сохранить настройки",
                                         command=self.save_settings,
                                         bg=config[self.theme]["BACKGROUND_COLOR"],
                                         fg=config[self.theme]["FONT_COLOR"])

        path_lb.grid(row=0, column=0, padx=5, pady=5)
        path_entry.grid(row=0, column=1, padx=5, pady=5)
        theme_choose_cb.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        save_settings_button.grid(row=1, column=1, padx=5, pady=5)

    def set_styles(self):
        """
        Настраивает стили виджетов для приложения.
        """
        style = ttk.Style(self)
        style.theme_create('main_theme', parent='alt', settings={})
        style.theme_use('main_theme')
        style.configure(
            "main.TLabel",
            background=config[self.theme]["BACKGROUND_COLOR"],
            foreground=config[self.theme]["FONT_COLOR"]
        )
        style.configure(
            "main.TButton",
            background=config[self.theme]["BACKGROUND_COLOR"],
            foreground=config[self.theme]["FONT_COLOR"]
        )
        style.configure(
            'main.TCombobox',
            background=config['theme1']['BACKGROUND_COLOR'],
            foreground=config['theme1']['FONT_COLOR'],
            fieldbackground=config['theme1']['FIELD_BG'],
            selectbackground=config['theme1']['SELECT_BG'],
            selectforeground=config['theme1']['SELECT_FG']
        )
        style.configure(
            "main.TEntry",
            background=config[self.theme]["ACCENT_COLOR_LIGHT"]
        )
        style.configure(
            "main.TFrame",
            background=config[self.theme]["BACKGROUND_COLOR"]
        )
        style.configure(
            'lefttab.TNotebook',
            tabposition='wn',
            background=config[self.theme]["BACKGROUND_COLOR_DARK"]
        )
        style.configure(
            'lefttab.TNotebook.Tab',
            padding=(5, 5, 5, 5),
            font=('Arial', 10),
            width=43,
            background=config[self.theme]["BACKGROUND_COLOR_DARK"],
            foreground=config[self.theme]["FONT_COLOR"]
        )

        style.map('lefttab.TNotebook.Tab',
                  background=[("selected",
                               config[self.theme]["BACKGROUND_COLOR"])],
                  foreground=[('selected',
                               config[self.theme]["ACCENT_COLOR_LIGHT"])])
        style.configure(
            "main.Treeview",
            background=config[self.theme]["BACKGROUND_COLOR"],
            foreground=config[self.theme]["FONT_COLOR"],
            fieldbackground=config['theme1']['FIELD_BG']
        )
        style.map('main.Treeview',
                  background=[('selected', config[self.theme]["SELECT_BG"])],
                  foreground=[('selected', config[self.theme]["SELECT_FG"])]
                  )
        style.configure("main.Treeview.Heading",
                        background=config[self.theme]["BACKGROUND_COLOR_DARK"],
                        foreground=config[self.theme]["FONT_COLOR"]
                        )
        style.configure(
            'main.TRadiobutton',
            background=config[self.theme]["BACKGROUND_COLOR"],
            foreground=config[self.theme]["ACCENT_COLOR"]
        )

    def delete_update(self, index, table, frame):
        """
        Удаляет строку с заданным индексом из таблицы и обновляет таблицу.

        Аргументы:
        - index: str - индекс строки, которую нужно удалить.
        - table: ttk.Treeview - таблица, из которой нужно удалить строку.
        - frame: tk.Frame - рамка, в которой расположена таблица.
        """
        global data
        data = delete_row(data, int(index) - 1)
        table.destroy()
        table = ttk.Treeview(frame)
        self.create_report_from_dataframe(data, table)
        for column in table["columns"]:
            table.column(column, width=int(
                config[self.theme]["FRAME_WIDTH"] / 10))
        table.update()
        table.grid(row=1, column=0, columnspan=3)

    def save_settings(self):
        """
        Сохраняет настройки, введенные пользователем.
        """
        config["db"]["path"] = self.path_db.get()
        self.theme = self.theme_choose.get()
        config["theme_now"] = self.theme
        config_path = os.path.join(os.path.dirname(__file__), '..', 'scripts',
                                   'config.json')
        with open(config_path, 'w', encoding="utf-8") as config_file:
            json.dump(config, config_file, ensure_ascii=False, indent=4)

    def next_question(self, last_answer, question_label, sex, direction,
                      university, course):
        """
        Переходит к следующему вопросу в тесте и обновляет результаты ответов.

        Аргументы:
        - last_answer: str - последний выбранный ответ.
        - question_label: ttk.Label - метка с текущим вопросом.
        - sex: str - пол пользователя.
        - direction: str - выбранное направление.
        - university: str - выбранный университет.
        - course: str - выбранный курс.
        """
        if self.current_question < len(config["questions"]):
            if config["questions"][self.current_question]["axis"] == "x+":
                self.new_answer['x'] = self.new_answer['x'] + \
                                       config["options"][last_answer]
            elif config["questions"][self.current_question]["axis"] == "x-":
                self.new_answer['x'] = self.new_answer['x'] - \
                                       config["options"][last_answer]
            elif config["questions"][self.current_question]["axis"] == "y+":
                self.new_answer['y'] = self.new_answer['y'] + \
                                       config["options"][last_answer]
            elif config["questions"][self.current_question]["axis"] == "y-":
                self.new_answer['y'] = self.new_answer['y'] - \
                                       config["options"][last_answer]
            elif config["questions"][self.current_question]["axis"] == "z+":
                self.new_answer['z'] = self.new_answer['z'] + \
                                       config["options"][last_answer]
            elif config["questions"][self.current_question]["axis"] == "z-":
                self.new_answer['z'] = self.new_answer['z'] - \
                                       config["options"][last_answer]
            self.current_question += 1
            if self.current_question < len(config["questions"]):
                question_label.config(
                    text=config["questions"][self.current_question]["question"]
                )
        elif self.current_question == len(config["questions"]):
            question_label.config(
                text="Тест пройден! " +
                     f"Ваш результат: x={self.new_answer['x']}," +
                     f" y={self.new_answer['y']}, z={self.new_answer['z']} " +
                     "Нажмите на кнопку, чтобы пройти снова!!!!!!!!!")
            print(
                "Тест пройден! " +
                f"Ваш результат: x={self.new_answer['x']}," +
                f" y={self.new_answer['y']}, z={self.new_answer['z']} " +
                "Нажмите на кнопку, чтобы пройти снова!!!!!!!!!")
            self.new_answer['x'] = [self.new_answer['x']]
            self.new_answer['y'] = [self.new_answer['y']]
            self.new_answer['z'] = [self.new_answer['z']]
            self.new_answer["id"] = data.iloc[-1]['id'] + 1
            self.new_answer["gender"] = sex
            self.new_answer["field"] = direction
            self.new_answer["university"] = university
            self.new_answer["course"] = course
            data.append(pd.DataFrame(self.new_answer), ignore_index=True)
            save_to_file(data)
            self.current_question += 1
        else:
            question_label.config(text=self.questions[0]["question"])
            self.new_answer = {
                'id': [],
                'gender': [],
                'field': [],
                'university': [],
                'course': [],
                'x': 0,
                'y': 0,
                'z': 0
            }
            self.current_question = 0

    def create_report_from_dataframe(self, df, f3_output):
        """
        Создает отчет из данных DataFrame и отображает его в виджете Treeview.

        Аргументы:
        - df: pandas.DataFrame - исходные данные.
        - f3_output: ttk.Treeview - виджет Treeview для отображения отчета.
        """
        f3_output.delete(*f3_output.get_children())

        f3_output["columns"] = list(df.columns)
        f3_output.column("#0", width=0, minwidth=0, stretch=False)

        for column in df.columns:
            f3_output.column(column, width=160, minwidth=50, stretch=True)
            f3_output.heading(column, text=column, anchor='w')

        for index, row in df.iterrows():
            values = tuple(row[column] for column in df.columns)
            f3_output.insert("", "end", values=values)

    def bar(self, frame, data, x_column, y_column, row, column, columnspan):
        """
        Функция создает кластеризованную столбчатую диаграмму (bar plot) с 
        использованием библиотеки matplotlib.pyplot.

        Кластеризованная столбчатая диаграмма показывает сравнение значений 
        между различными категориями (x_column) и подкатегориями (y_column) 
        с помощью столбцов, разделенных по категориям.

        Параметры:
        frame (tkinter.Frame): Фрейм tkinter, в котором нужно разместить 
        столбчатую диаграмму.
        data (pandas.DataFrame): DataFrame, содержащий данные.
        x_column (str): Имя столбца в data, представляющего категории 
        (ось x) на столбчатой диаграмме.
        y_column (str): Имя столбца в data, представляющего подкатегории 
        (ось y) на столбчатой диаграмме.
        row (int): Номер строки в frame, в которой будет размещена столбчатая 
        диаграмма.
        column (int): Номер столбца в frame, в котором будет размещена 
        столбчатая диаграмма.
        columnspan (int): Ширина столбчатой диаграммы в frame (в количестве 
                                                               столбцов).

        Возвращает:
        None. Функция отображает кластеризованную столбчатую диаграмму в 
        указанном фрейме.
        """
        grouped_data = data.groupby(
            [x_column, y_column]).size().reset_index(name='counts')

        fig, ax = plt.subplots()

        for label, df in grouped_data.groupby(y_column):
            ax.bar(df[x_column], df['counts'], label=label)

        ax.set_title('Кластеризованная столбчатая диаграмма')
        ax.set_xlabel(x_column)
        # Измените 'counts' на то, что вы хотите отобразить
        ax.set_ylabel('counts')
        ax.legend(title=y_column)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()

        canvas.get_tk_widget().grid(row=row, column=column,
                                    columnspan=columnspan)

    def plot_hist(self, frame, df, qual_attr, quant_attr, row,
                  column, columnspan):
        """
        Функция создает гистограмму для пары "количественный атрибут - 
        качественный атрибут" с использованием библиотеки matplotlib.

        Гистограмма показывает распределение значений количественного 
        атрибута для каждого уровня качественного атрибута. Это позволяет 
        визуально оценить различия в распределении количественного 
        атрибута между различными группами, определенными качественным 
        атрибутом.

        Параметры:
        frame (tkinter.Frame): Фрейм tkinter, в котором нужно разместить 
        диаграмму.
        df (pandas.DataFrame): DataFrame, содержащий данные.
        qual_attr (str): Имя столбца в df, представляющего качественный 
        атрибут.
        quant_attr (str): Имя столбца в df, представляющего количественный 
        атрибут.
        row (int): Номер строки в окне tkinter, в которой будет размещена 
        гистограмма.
        column (int): Номер столбца в окне tkinter, в котором будет размещена 
        гистограмма.
        columnspan (int): Ширина гистограммы в окне tkinter (в количестве 
                                                             столбцов).

        Возвращает:
        None. Функция отображает гистограмму, но ничего не возвращает.
        """
        # Получаем уникальные значения качественного атрибута
        qual_attr_values = df[qual_attr].unique()

        # Создаем список цветов для каждого уровня качественного атрибута
        colors = plt.cm.rainbow(np.linspace(0, 1, len(qual_attr_values)))

        # Создаем объект Figure и AxesSubplot
        fig, ax = plt.subplots()

        # Для каждого уровня качественного атрибута строим гистограмму
        for i, qual_value in enumerate(qual_attr_values):
            # Выбираем только те строки, где качественный атрибут равен текущему значению
            data = df.loc[df[qual_attr] == qual_value, quant_attr]

            # Строим гистограмму
            ax.hist(data, bins=10, alpha=0.5,
                    label=qual_value, color=colors[i])

        # Добавляем легенду
        ax.legend(loc='upper right')

        # Устанавливаем заголовок
        ax.set_title(f'Distribution of {quant_attr} by {qual_attr}')

        # Устанавливаем метки осей
        ax.set_xlabel(quant_attr)
        ax.set_ylabel('Frequency')

        # Отображаем гистограмму в tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().grid(row=row, column=column,
                                    columnspan=columnspan)

    def create_boxplot(self, frame, df, qual_attr, quant_attr, row,
                       column, columnspan):
        """
        Функция создает ящиковую диаграмму (boxplot) для пары "количественный 
        атрибут - качественный атрибут" с использованием библиотеки 
        matplotlib.pyplot.

        Ящиковая диаграмма позволяет визуализировать распределение значений 
        количественного атрибута для каждого уровня качественного атрибута. 
        Каждый ящик представляет собой интерквартильный размах, который 
        показывает, где находятся основные 50% значений, а отдельные точки 
        могут представлять выбросы.
        """
        # Создаем список уникальных значений качественного атрибута
        qual_attr_values = df[qual_attr].unique()

        data = [df[df[qual_attr] == value][quant_attr]
                for value in qual_attr_values]

        # Создаем ящиковую диаграмму
        fig, ax = plt.subplots()
        ax.boxplot(data)

        # Настраиваем оси и заголовок диаграммы
        ax.set_xticklabels(qual_attr_values)
        ax.set_xlabel(qual_attr)
        ax.set_ylabel(quant_attr)
        ax.set_title(f'Ящиковая диаграмма для {quant_attr} и {qual_attr}')

        # Размещаем диаграмму в указанном фрейме tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=row, column=column,
                                    columnspan=columnspan)

    def plot_scatter(self, frame, df, qual_attr, quant_attr1, quant_attr2,
                     row, column, columnspan):
        """
        Функция создает точечную диаграмму (scatter plot) для двух 
        количественных атрибутов и одного качественного атрибута с 
        использованием библиотеки matplotlib.pyplot.

        Точечная диаграмма показывает взаимосвязь между двумя 
        количественными атрибутами, представленную в виде точек 
        на плоскости. Каждая точка имеет координаты, определенные 
        значениями двух количественных атрибутов, а также цвет или 
        форму, соответствующую уровню качественного атрибута.

        Параметры:
        - frame (tkinter.Frame): Фрейм tkinter, в котором нужно разместить 
        точечную диаграмму.
        - df (pandas.DataFrame): DataFrame, содержащий данные.
        - qual_attr (str): Имя столбца в df, представляющего качественный 
        атрибут.
        - quant_attr1 (str): Имя первого столбца в df, представляющего 
        количественный атрибут.
        - quant_attr2 (str): Имя второго столбца в df, представляющего 
        количественный атрибут.
        - row (int): Номер строки в frame, в которой будет размещена 
        точечная диаграмма.
        - column (int): Номер столбца в frame, в котором будет размещена 
        точечная диаграмма.
        - columnspan (int): Ширина точечной диаграммы в frame (в количестве 
                                                               столбцов).

        Возвращает:
        None. Функция отображает точечную диаграмму, но ничего не возвращает.
        """
        # Создаем список уникальных значений качественного атрибута
        qual_attr_values = df[qual_attr].unique()

        # Создаем цветовую карту для уровней качественного атрибута
        colors = plt.cm.get_cmap('Set1', len(qual_attr_values))

        # Создаем точечную диаграмму
        fig, ax = plt.subplots()
        for i, value in enumerate(qual_attr_values):
            x = df[df[qual_attr] == value][quant_attr1]
            y = df[df[qual_attr] == value][quant_attr2]
            ax.scatter(x, y, color=colors(i), label=value)

        # Настраиваем оси и заголовок диаграммы
        ax.set_xlabel(quant_attr1)
        ax.set_ylabel(quant_attr2)
        ax.set_title(
            f'Точечня диаграмма для {quant_attr1}, {quant_attr2}, {qual_attr}')
        ax.legend()

        # Размещаем диаграмму в указанном фрейме tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=row, column=column,
                                    columnspan=columnspan)
