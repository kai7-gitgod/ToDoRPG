from nicegui import ui
import home_page
import pages.user_homepage

def backToUserHomepage():
    pages.user_homepage.selected_questid = 0
    ui.run_javascript('window.location.href = "/user_homepage";')



@ui.page("/quest_editpage")
def render():
    if(home_page.selected_userid != 0 and pages.user_homepage.selected_questid != 0):
        selected_quest = pages.user_homepage.getQuest()
        ui.label(("Du bearbeitest jetzt die QuestID: ", selected_quest.questid))
        ui.label(("Beschreibung: ", selected_quest.beschreibung))
        ui.label(("Erfahrungspunkte: ", selected_quest.exp))
        ui.label(("Abschlussdatum: ", selected_quest.dtm))
        ui.label(("Schwierigkeit: ", selected_quest.diff))
        ui.button("Quest abschließen", on_click=lambda:pages.user_homepage.completeQuest())
        ui.button("Zurück", on_click=lambda:backToUserHomepage())
    else:

        ui.run_javascript('window.location.href = "/";')

def startEditQuest():
        if(home_page.selected_userid != 0 and pages.user_homepage.selected_questid != 0):
            user = home_page.getUser()
            selected_quest = pages.user_homepage.getQuest()
            with ui.dialog(value=True).props('persistent') as dialog, ui.card():
                ui.label(("Quest bearbeiten")).style("font-size: 20px; font-weight: bold;")
                ui.label(("ID: ", selected_quest.questid))
                ui.label(("Beschreibung: ", selected_quest.beschreibung))
                ui.label(("Erfahrungspunkte: ", selected_quest.exp))
                ui.label(("Abschlussdatum: ", selected_quest.dtm))
                ui.label(("Schwierigkeit: ", selected_quest.diff))
                with ui.row():
                    ui.button("Quest abschließen", color="green" ,icon="done", on_click=lambda:pages.user_homepage.completeQuest(dialog))
                    ui.button("Zurück", on_click=lambda: dialog.close(), color="red", icon="cancel")
        else:
            ui.notify("Wähle eine Quest aus")
