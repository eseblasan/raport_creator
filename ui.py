import flet as ft
import tkinter as tk
import validators
from tkinter import filedialog
from datetime import date
from create_report import add_link_to_data, create_report


async def window(page: ft.Page):
    page.title = "Ivan report Creator"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 700
    report_data = {}

    added_links_view = ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, expand=True)

    project_name = ft.TextField(
        label="Project Name",
        border_color=ft.Colors.BLUE_400,
        prefix_icon=ft.Icons.WORK_OUTLINE
    )

    link_input = ft.TextField(
        label="Commit Link or text",
        hint_text="Paste your link or text here...",
        expand=True
    )

    def on_clear_click(e):
        added_links_view.controls.clear()
        report_data.clear()
        project_name.value = ""
        link_input.value = ""
        page.update()

    async def on_add_click(e):
        if link_input.value and project_name.value:

            if project_name.value not in report_data:
                report_data[project_name.value] = []

            add_link_to_data(project_name.value, link_input.value, report_data)

            new_ui_controls = []
            sorted_projects = sorted(report_data.keys())

            for proj in sorted_projects:
                for item in report_data[proj]:

                    icon_type = ft.Icons.COMMIT if str(item).startswith("http") else ft.Icons.NOTES

                    new_commit = ft.ListTile(
                        leading=ft.Icon(icon_type),
                        title=ft.Text(f"{proj} | {item}"),
                    )
                    new_ui_controls.append(new_commit)

            added_links_view.controls = new_ui_controls

            link_input.value = ""
            await link_input.focus()
            page.update()

    link_input.on_submit = on_add_click

    def on_export_click(e):
        current_date = date.today().strftime("%d-%m-%Y")
        dynamic_name = f"report_{current_date}.xlsx"

        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)


        file_path = filedialog.asksaveasfilename(
            title="Where save raport?",
            initialfile=dynamic_name,
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )

        root.destroy()

        if file_path:
            try:
                create_report(report_data, file_path)
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Отчет сохранен!\n{file_path}"),
                    bgcolor=ft.Colors.GREEN_700
                )
                page.snack_bar.open = True
            except Exception as ex:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Ошибка при сохранении: {ex}"),
                    bgcolor=ft.Colors.RED_700
                )
                page.snack_bar.open = True

            page.update()

    page.add(
        ft.Text("Monthly Report Generator", size=25, weight=ft.FontWeight.BOLD),
        project_name,
        ft.Divider(height=20, color="transparent"),

        ft.Row([
            link_input,
            ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=on_add_click),
        ]),

        ft.Text("Added Commits:", size=16, weight=ft.FontWeight.W_500),

        ft.Container(
            content=added_links_view,
            border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=10,
            padding=10,
            expand=True
        ),

        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.ElevatedButton(
                    "Export Report",
                    icon=ft.Icons.FILE_DOWNLOAD,
                    expand=True,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=on_export_click
                ),
                ft.ElevatedButton(
                    "Generate Report",
                    expand=True,

                ),
                ft.ElevatedButton(
                    "Clear",
                    icon=ft.Icons.DELETE_OUTLINE,
                    on_click=on_clear_click,
                    expand=True,
                    style=ft.ButtonStyle(
                        color=ft.Colors.RED_400,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                ),
            ]
        )
    )