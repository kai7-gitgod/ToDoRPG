from nicegui import ui
import pages.user_homepage
import home_page

def backToUserHomepage():
    pages.user_homepage.selected_questid = 0
    ui.run_javascript('window.location.href = "/user_homepage";')

def checkQuest(beschreibung, dtm, diff, dialog):
    if(beschreibung != "" and dtm != "" and diff != ""):
        exp = 0
        match(diff):
            case "Leicht":
                exp = 30
            case "Mittel":
                exp = 60
            case "Schwer":
                exp = 100

        pages.user_homepage.createQuest(beschreibung, exp, dtm, diff)
        dialog.close()
        ui.navigate.to("/user_homepage")
    else:
        ui.notify("Bitte alle Felder bearbeiten")

def startQuestCreation():
    if(home_page.selected_userid != 0):
        user = home_page.getUser()
        with ui.dialog(value=True).props('persistent') as dialog, ui.card():
            ui.label(("Neue Quest erstellen")).classes("text-lg")
            ui_input_beschreibung = ui.input(label="Beschreibung")
            with ui.input('Date') as date:
                with ui.menu().props('no-parent-event') as menu:
                    with ui.date().bind_value(date):
                        with ui.row().classes('justify-end'):
                            ui.button('Close', on_click=menu.close).props('flat')
                with date.add_slot('append'):
                    ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')
            ui_input_diff = ui.select(["Leicht", "Mittel", "Schwer"], label="Schwierigkeit")
            with ui.row():
                ui.button("Erstellen", on_click=lambda: checkQuest(ui_input_beschreibung.value, date.value, ui_input_diff.value, dialog), color="green", icon="done")
                ui.button("Abbrechen", on_click=lambda: dialog.close(), color="red", icon="cancel")