import pandas as pd
from datetime import date
from openpyxl import load_workbook
from openpyxl.styles import Font


def add_link_to_data(group_name: str, link: str, data) -> None:
    data[group_name].append(link)


def create_report(data: dict, file_path: str) -> str:
    rows = []
    for group_name, links in data.items():
        row = [group_name] + links
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_excel(file_path, index=False, header=False)

    wb = load_workbook(file_path)
    ws = wb.active

    for row in ws.iter_rows():
        for i, cell in enumerate(row):

            # Пропускаем первую колонку (имя проекта)
            if i == 0:
                continue

            # Если в ячейке есть любой текст
            if cell.value:
                url = str(cell.value).strip()

                # Если юзер забыл написать http/https, добавляем сами
                if not url.startswith("http"):
                    url = "https://" + url

                # Прячем ссылку за порядковой цифрой
                cell.value = str(i)
                cell.hyperlink = url
                cell.font = Font(color="0000FF", underline="single")

    wb.save(file_path)
    return file_path


if __name__ == "__main__":
    group_name = ""
    links = []
    data = {
        group_name: []
    }

    for link in links:
        add_link_to_data(group_name, link, data)

    # Генерируем тестовое имя файла с сегодняшней датой
    test_file_name = "report_" + date.today().strftime("%d-%m-%Y") + ".xlsx"
    create_report(data, test_file_name)
    print(f"Тестовый файл {test_file_name} успешно создан!")