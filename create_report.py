import pandas as pd
from datetime import date
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter


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


    center_alignment = Alignment(horizontal="center", vertical="center")

    for row in ws.iter_rows():
        for i, cell in enumerate(row):


            cell.alignment = center_alignment

            if i == 0:
                continue

            if cell.value:
                url = str(cell.value).strip()
                if not url.startswith("http"):
                    url = "https://" + url

                cell.value = str(i)
                cell.hyperlink = url
                cell.font = Font(color="0000FF", underline="single")

    for col in ws.columns:
        max_length = 0
        column_letter = get_column_letter(col[0].column)

        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass

        adjusted_width = (max_length + 4)
        ws.column_dimensions[column_letter].width = adjusted_width

    wb.save(file_path)
    return file_path