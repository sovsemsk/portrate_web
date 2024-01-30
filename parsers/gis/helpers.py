import json
import locale
import re

from datetime import datetime
from typing import Union


class ParserHelper:
    @staticmethod
    def list_to_num(l: list) -> int:
        """
        Преобразует пришедший массив в первое попавшееся число
        @param l: ['321fdfd','fdfd']
        @return: Число 321
        """
        if len(l) <= 0:
            raise IndexError("Empty list")
        numbers: list = [x for x in re.findall(r"-?\d+\.?\d*", "".join(l))]
        if not numbers:
            raise ValueError("No numbers")
        return int(float(numbers[0]))

    @staticmethod
    def format_rating(l: list) -> float:
        """
        Форматирует рейтинг в число с плавающей точкой
        @param l: Массив значений ['1','.','5']
        @return: Число с плавающей точкой 1.5
        """
        if len(l) <= 0:
            return 0
        return float("".join(x.text for x in l).replace(",", "."))

    @staticmethod
    def write_json_txt(result, file) -> None:
        """
        Записать новый файл JSON
        :param result: JSON Объект который нужно записать
        :param file: Название файла (вместе с .json)
        :return: None
        """
        with open(file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

    @staticmethod
    def form_date(date_string: str) -> float:
        """
        Приводим дату в формат Timestamp
        :param date_string: Дата в формате %d %b %Y
        :return: Дата в формате Timestamp
        """

        splitted_date_string = date_string.replace(", отредактирован", "").split()
        splitted_date_string[1] = splitted_date_string[1][:3]
        cutted_date_string = " ".join(splitted_date_string).replace("мая", "май")

        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

        datetime_object: datetime = datetime.strptime(
            cutted_date_string, "%d %b %Y"
        )

        return datetime_object.timestamp()

    @staticmethod
    def get_count_star(review_stars: list) -> Union[float, int]:
        """
        Считаем рейтинг по звездам
        :param review_stars: Массив элементов звезд рейтинга
        :return: Рейтинг
        """

        return float(len(review_stars))
