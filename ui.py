import flet as ft
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
        label="Commit Link",
        hint_text="Paste your link here...",
        expand=True
    )
    def on_clear_click(e):
        added_links_view.controls.clear()
        report_data.clear()
        page.update()

    ft.ElevatedButton(
        "Clear",
        icon= ft.Icons.DELETE_OUTLINE,
        on_click=on_clear_click,
        style=ft.ButtonStyle(
            color=ft.Colors.RED_400,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
    )

    async def on_add_click(e):
        if link_input.value and project_name.value:
            if project_name.value not in report_data:
                report_data[project_name.value] = []

            add_link_to_data(project_name.value, link_input.value, report_data)

            new_commit = ft.ListTile(
                leading=ft.Icon(ft.Icons.COMMIT),
                title=ft.Text(link_input.value),
            )

            added_links_view.controls.append(new_commit)


            link_input.value = ""
            await link_input.focus()
            page.update()

    link_input.on_submit = on_add_click



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

        ft.ElevatedButton(
            "Generate Report",
            icon=ft.Icons.FILE_DOWNLOAD,
            width=page.window_width,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=lambda _: print(create_report(report_data))
        ),
        ft.ElevatedButton(
            "Clear",
            icon=ft.Icons.DELETE_OUTLINE,
            on_click=on_clear_click,
            style=ft.ButtonStyle(
                color= ft.Colors.RED_400,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
        )


    )


