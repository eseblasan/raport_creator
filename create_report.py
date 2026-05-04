import pandas as pd
from datetime import date
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter


def add_link_to_data(group_name: str, link: str, data) -> None:
    data[group_name].append(link)


def create_report(data: dict) -> str:
    file_name = "report_" + date.today().strftime("%d-%m-%Y") + ".xlsx"

    rows = []
    for group_name, links in data.items():
        row = [group_name] + links
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_excel(file_name, index=False, header=False)


    wb = load_workbook(file_name)
    ws = wb.active

    for row in ws.iter_rows():
        for i, cell in enumerate(row):

            if i == 0:
                continue
            if cell.value and str(cell.value).startswith("http"):
                url = cell.value
                cell.value = str(i)
                cell.hyperlink = url
                cell.font = Font(color="0000FF", underline="single")

    wb.save(file_name)
    return file_name


if __name__ == "__main__":
    group_name = "group"
    links = [
        "https://rt.pornhub.com/view_video.php?viewkey=69ee7e8961a29",
        "https://example.com/page2",
        "https://example.com/page3",
    ]
    data = {
        group_name: []
            }

    for link in links:
        add_link_to_data(group_name, link, data)

    create_report(data)