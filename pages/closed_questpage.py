from nicegui import ui
import pages.user_homepage
import home_page

def backToUserHomepage():
    pages.user_homepage.selected_questid = 0
    ui.run_javascript('window.location.href = "/user_homepage";')
ui_radio_quests_comp = 0
ui_radio_quests_fail = 0

selected_quest_comp = 0
selected_quest_fail = 0

def setCompQuestID():
    global selected_quest_comp
    global ui_radio_quests_comp
    if(len(pages.user_homepage.completedquests) != 0):
            selected_quest_comp = ui_radio_quests_comp.value[0]

def setFailQuestID():
    global selected_quest_fail
    global ui_radio_quests_fail
    if(len(pages.user_homepage.failedquests) != 0):
            selected_quest_fail = ui_radio_quests_fail.value[0]

def executeDelete():
    setCompQuestID()
    setFailQuestID()
    pages.user_homepage.deleteQuest(selected_quest_comp, selected_quest_fail)

def test():
    global ui_radio_quests_fail
    print(ui_radio_quests_fail.value[0])
@ui.page("/quest_closedpage")
def render():
    if(home_page.selected_userid != 0):
        pages.user_homepage.fillQuestLists()
        ui.label("Erfolgreich abgeschlossene Quests:")
        if(len(pages.user_homepage.completedquests) != 0):
            global ui_radio_quests_comp
            ui_radio_quests_comp = ui.radio([""])
            ui_radio_quests_comp.options.clear()

            for quest in pages.user_homepage.completedquests:
                ui_radio_quests_comp.options.append((quest.questid, ". | Beschreibung: ", quest.beschreibung, " | EXP: ", quest.exp, " | Ablaufdatum: ", quest.dtm, " | Schwierigkeit: ", quest.diff, " Status: ", quest.state))
                ui_radio_quests_comp.update()
        else:
            ui.label("Noch keine erfolgreich abgeschlossenen Quests vorhanden")

        ui.label("Fehlgeschlagene Quests:")
        if(len(pages.user_homepage.failedquests) != 0):
            global ui_radio_quests_fail
            ui_radio_quests_fail = ui.radio([""])
            ui_radio_quests_fail.options.clear()

            for quest in pages.user_homepage.failedquests:
                ui_radio_quests_fail.options.append((quest.questid, ". | Beschreibung: ", quest.beschreibung, " | EXP: ", quest.exp, " | Ablaufdatum: ", quest.dtm, " | Schwierigkeit: ", quest.diff, " Status: ", quest.state))
                ui_radio_quests_fail.update()
        else:
            ui.label("Noch keine fehlgeschlagenen Quests vorhanden")

        ui.button("Markierte Quests löschen", on_click=lambda:executeDelete())
        ui.button("Zurück", on_click=lambda:backToUserHomepage())
    else:
        ui.run_javascript('window.location.href = "/";')