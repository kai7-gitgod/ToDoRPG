from nicegui import ui
import sqlite3
import home_page
from quest import quest
import pages.create_questpage
import pages.edit_questpage
from datetime import date, datetime
import os

questlist = []
completedquests = []
failedquests = []
openquests = []

selected_questid = 0
radio_user = None
ui_show_quests = None
ui_create_quest = None
ui_go_back = None

user_homepage_label = None

def getQuest():
    for quest in questlist:
        if(quest.questid == selected_questid):
            return quest
        
    return 0

def checkQuestDate():
    heute = date.today()
    conn = sqlite3.connect("userdata.db")
    cursor = conn.cursor()
    for quest in openquests:
          pruef_datum = datetime.strptime(quest.dtm, "%Y-%m-%d").date()
          if(pruef_datum < heute):
                cursor.execute("UPDATE quests SET userid = ?, beschreibung = ?, erfahrungspunkte = ?, abschlussdatum = ?, schwierigkeit = ?, status = ? WHERE questid = ?",
                        (quest.userid, quest.beschreibung, quest.exp, quest.dtm, quest.diff, "fehlgeschlagen", quest.questid))
    fillQuestLists()
    conn.commit()
    conn.close()  

def completeQuest(dialog):
    selected_quest = getQuest()
    conn = sqlite3.connect("userdata.db")
    cursor = conn.cursor()

    selected_user = home_page.getUser()
    selected_quest = getQuest()
    exp_quest = selected_quest.exp
    exp_user = selected_user.exp

    if(exp_user + exp_quest < 100):
        selected_user.exp = exp_user + exp_quest
    else:
        exp_diff = (exp_user + exp_quest) - 100
        selected_user.exp = exp_diff
        selected_user.level += 1

    cursor.execute("UPDATE users SET name = ?, level = ?, erfahrungspunkte = ? WHERE userid = ?",
                        (selected_user.name, selected_user.level, selected_user.exp, selected_user.userid))
    cursor.execute("UPDATE quests SET userid = ?, beschreibung = ?, erfahrungspunkte = ?, abschlussdatum = ?, schwierigkeit = ?, status = ? WHERE questid = ?",
                        (selected_quest.userid, selected_quest.beschreibung, selected_quest.exp, selected_quest.dtm, selected_quest.diff, "abgeschlossen", selected_quest.questid))

    conn.commit()
    conn.close()
    ui.notify("Quest wurde als abgeschlossen markiert!") 
    dialog.close()
    ui.navigate.to("/user_homepage")

def deleteQuest(comp_questid, fail_questid):
    conn = sqlite3.connect("userdata.db")
    cursor = conn.cursor()

    if(comp_questid != 0):
        cursor.execute("DELETE FROM quests WHERE questid = ?", (comp_questid,))

    if(fail_questid != 0):
        cursor.execute("DELETE FROM quests WHERE questid = ?", (fail_questid,))

    conn.commit()
    conn.close()
    ui.run_javascript('window.location.href = "/user_homepage";')

def fillQuestLists():
    conn = sqlite3.connect("userdata.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quests")
    rows = cursor.fetchall()

    conn.commit()
    questlist.clear()
    completedquests.clear()
    openquests.clear()
    failedquests.clear()

    for row in rows:
        meine_quest = quest(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        if(meine_quest.userid == home_page.selected_userid):
                questlist.append(meine_quest)
                if meine_quest.state == "abgeschlossen":
                        completedquests.append(meine_quest)
                elif meine_quest.state == "fehlgeschlagen":
                        failedquests.append(meine_quest)
                else:
                        openquests.append(meine_quest)
    
    conn.close()

def saveQuestsInDB():
    conn = sqlite3.connect("userdata.db")
    cursor = conn.cursor()
    for aufgabe in questlist:
        cursor.execute("UPDATE quests SET userid = ?, beschreibung = ?, erfahrungspunkte = ?, abschlussdatum = ?, schwierigkeit = ?, status = ? WHERE questid = ?",
                        (aufgabe.userid, aufgabe.beschreibung, aufgabe.exp, aufgabe.dtm, aufgabe.diff, aufgabe.state, aufgabe.questid))

    conn.commit()
    conn.close() 

def setSelectedQuest(questid):
        global selected_questid
        selected_questid = questid

def createQuest(beschreibung, exp, date, diff):
    if(beschreibung != "" and exp != 0 and date != 0 and diff != ""):
        conn = sqlite3.connect("userdata.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO quests (userid, beschreibung, erfahrungspunkte, abschlussdatum, schwierigkeit, status) VALUES (?, ?, ?, ?, ?, ?)", [home_page.selected_userid, beschreibung, exp, date, diff, "offen"])

        conn.commit()
        conn.close()
        ui.notify("Quest " + beschreibung + " wurde erstellt")
    else:
        ui.notify("Trage in alle Felder etwas ein")

def showOpenQuests():
    radio_user.clear()

    fillQuestLists()
        
    for quest in openquests:
        radio_user.options.append((quest.questid, ". | Beschreibung: ", quest.beschreibung, " | EXP: ", quest.exp, " | Ablaufdatum: ", quest.dtm, " | Schwierigkeit: ", quest.diff))
        radio_user.update()

def test():
     fillQuestLists()
     if(len(questlist) != 0):
        for quest in questlist:
                print(quest.questid, "", quest.userid, "", quest.beschreibung)
     else:
          print("keine quests für diesen user")

def backToHomePage():
      global selected_questid
      home_page.selected_userid = 0
      selected_questid = 0
      ui.run_javascript('window.location.href = "/";')

def sendToEditQuestPage():
      if(selected_questid != 0):
        ui.run_javascript('window.location.href = "/quest_editpage";')
      else:
        ui.notify("Wähle eine Quest aus")

def sendToCreateQuestPage():
     ui.run_javascript('window.location.href = "/quest_createpage";')

def showClosedQuests():
    if(len(completedquests) != 0 or len(failedquests) != 0):
        ui.run_javascript('window.location.href = "/quest_closedpage";')
    else:
         ui.notify("Es wurden noch keine Quests abgeschlossen")

@ui.page("/user_homepage", title="ToDoRPG")
def render():
        global radio_user
        global user_homepage_label
        global ui_show_quests
        global ui_create_quest
        global ui_go_back
        if(home_page.selected_userid != 0):
            with ui.header().style('background-color: #1e81b0; align-items: center;'):
                 ui.icon("person").style("font-size: 25px; color: black;")
                 ui.label(("Benutzer: ", home_page.getUser().name)).style("font-weight: bold; font-size: 25px; color: black;")
            user_homepage_label = ui.label((home_page.getUser().name, " | Level: ", home_page.getUser().level)) 
            fillQuestLists()
            if(len(openquests) != 0):
                checkQuestDate()
                radio_user = ui.radio([""], on_change=lambda:setSelectedQuest(radio_user.value[0]))
                radio_user.options.clear()
                showOpenQuests()
                ui.button("Quest bearbeiten", on_click=lambda:pages.edit_questpage.startEditQuest())
            else:
                ui.label("Keine offenen Quests vorhanden")

            ui_create_quest = ui.button("Neue Quest erstellen", on_click=lambda:pages.create_questpage.startQuestCreation())
            ui.button("Abgeschlossene Quests anzeigen", on_click=lambda:showClosedQuests())
            ui.button("Zurück", on_click=lambda:backToHomePage(), color="red")
        else:
            ui.navigate.to("/") 



