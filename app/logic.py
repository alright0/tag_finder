from bs4 import BeautifulSoup
import requests


def count_tags(link: str) -> (dict, int):
    """Функция принимает ссылку и возвращает словарь, содержащий уникальные
    теги
    """
    try:
        html = requests.get(link)

        soup = BeautifulSoup(html.text, "html.parser")

        tags, counts, result = [], {}, {}

        # найти все теги и составить множество уникальных
        for tag in soup.find_all(True):
            tags.append(tag.name)
        unique_tags = set(tags)

        # Перебрать множество уникальных тегов и найти вхождения тегов
        for unique_tag in unique_tags:
            counts[unique_tag] = 0
            for every_tag in tags:
                if unique_tag == every_tag:
                    counts[unique_tag] += 1

            # Если количество тегов равно 1, получить для них список вложенных элементов
            if counts[unique_tag] == 1:
                result[unique_tag] = dict(
                    count=counts[unique_tag],
                    nested=len(list(soup.find(unique_tag).descendants)),
                )

    except Exception as e:
        return dict(error=str(e)), 422

    return result, html.status_code
