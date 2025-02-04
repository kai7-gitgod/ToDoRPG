from nicegui import ui
import sqlite3
import quest
from user import user
import pages.user_homepage
import pages.create_user
import pages.delete_user
from datetime import date

userlist = []

selected_userid = 0

def createDatabase():
    conn = sqlite3.connect("userdata.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        userid INTEGER PRIMARY KEY,
        name TEXT,
        level INTEGER,
        erfahrungspunkte INTEGER
    )
    """)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quests (
            questid INTEGER PRIMARY KEY AUTOINCREMENT,
            userid INTEGER NOT NULL,
            beschreibung TEXT NOT NULL,
            erfahrungspunkte INTEGER NOT NULL,
            abschlussdatum DATE,
            schwierigkeit TEXT CHECK(schwierigkeit IN ('Leicht', 'Mittel', 'Schwer')),
            status TEXT CHECK(status IN ('offen', 'abgeschlossen', 'fehlgeschlagen')),
            FOREIGN KEY (userid) REFERENCES users(userid)
        )
    ''')

def fillUserList():
    conn = sqlite3.connect("userdata.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    userlist.clear()

    for row in rows:
        mein_user = user(row[0], row[1], row[2], row[3])
        userlist.append(mein_user)
    
    conn.close()

def getUser():
    fillUserList()
    for benutzer in userlist:
        if(benutzer.userid == selected_userid):
            return benutzer
        
    return 0

def setSelectedUser(userid):
    global selected_userid
    selected_userid = userid

def createUser(name, level, exp):
    conn = sqlite3.connect("userdata.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (name, level, erfahrungspunkte) VALUES (?, ?, ?)", [name, level, exp])

    conn.commit()
    conn.close()

def createNewUser(name, ui_input_username):
    if name != "":
        createUser(name, 1, 0)
        fillUserList()
        ui.run_javascript('window.location.href = "/"')
        ui_input_username.set_value("")
        ui.notify("User " + name + " erstellt")
    else:
        ui.notify("Gib etwas in das Feld ein")

def sendToUserHomePage(userid):
    setSelectedUser(userid)
    if(selected_userid != 0):
        ui.navigate.to("/user_homepage")
    else:
        ui.notify("Wähle einen User aus")

def showDeletionPopUp(userid):
    setSelectedUser(userid)
    pages.delete_user.startUserDeletion()

def startRanking():
    if(len(userlist) != 0):
        ranked_users = sorted(userlist, key=lambda user: (user.level, user.exp), reverse=True)
        with ui.dialog(value=True).props('persistent') as dialog, ui.card():
            with ui.row().style("align-items: center;"):
                ui.icon("rocket_launch").style("font-size: 20px;")
                ui.label("Rangliste").style("font-size: 20px; font-weight: bold;")
            index = 1
            for user in ranked_users:
                match index:
                    case 1:
                        with ui.row().style('align-items: center;'):
                            ui.icon("star").style("color: gold;")
                            ui.label((index, ". ", user.name, " | Level: ", user.level, " Erfahrungspunkte: ", user.exp))
                    case 2:
                        with ui.row().style('align-items: center;'):
                            ui.icon("star").style("color: silver;")
                            ui.label((index, ". ", user.name, " | Level: ", user.level, " Erfahrungspunkte: ", user.exp))
                    case 3:
                        with ui.row().style('align-items: center;'):
                            ui.icon("star").style("color: #873e23;")
                            ui.label((index, ". ", user.name, " | Level: ", user.level, " Erfahrungspunkte: ", user.exp))
                    case _:
                        ui.label((index, ". ", user.name, " | Level: ", user.level, " Erfahrungspunkte: ", user.exp))
                index += 1
            ui.button("Zurück", on_click=lambda: dialog.close(), color="red", icon="cancel")
    else:
        ui.notify("Es gibt noch keine User")

@ui.page("/", title="ToDoRPG")
def render():
    global selected_userid
        
    fillUserList()
    selected_userid = 0
    with ui.header().style('background-color: #1e81b0;'):
        with ui.row().style('align-items: center;'):
            ui.icon("home").style('color: black; font-size: 25px;') 
            ui.label("Benutzerverwaltung").style("font-weight: bold; font-size: 25px; color: black;")
    with ui.row():
        ui.button("Neu Erstellen", color="green", icon="add", on_click=lambda:pages.create_user.startUserCreation())
        ui.button("Rangliste", color="gold", icon="rocket_launch", on_click=lambda:startRanking())
    if len(userlist) != 0:
        with ui.row():
            for user in userlist:
                with ui.card():
                    with ui.row().style('align-items: center;'):
                        ui.icon("person", size="2em")
                        ui.label(("Benutzer: ", user.name)).style("font-weight: bold;")
                        ui.button(icon="edit", on_click=lambda user=user: sendToUserHomePage(user.userid)).style("height: 25px; width: 50px; color:black;")
                        ui.button(icon="delete", color="red", on_click=lambda user=user: showDeletionPopUp(user.userid)).style("height: 25px; width: 50px; color: red;") 
                    ui.item(("Level: ", user.level))
                    ui.item(("Erfahrungspunkte: ", user.exp))
        