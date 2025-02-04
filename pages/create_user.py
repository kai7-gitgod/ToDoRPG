from nicegui import ui
import sqlite3

def startUserCreation():
    with ui.dialog(value=True).props('persistent') as dialog, ui.card():
        ui.label("Neuen User erstellen").classes("text-lg")
        ui_input_username = ui.input(label=("Name"), placeholder="Hier Username eingeben")
        with ui.row():
            ui.button("User anlegen", on_click=lambda: createUser(ui_input_username.value, dialog), color="green", icon="done")
            ui.button("Abbrechen", on_click=lambda: dialog.close(), color="red", icon="cancel")

def createUser(name, dialog):
    if(len(name) >= 3):
            conn = sqlite3.connect("userdata.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO users (name, level, erfahrungspunkte) VALUES (?, ?, ?)", [name, 1, 0])

            conn.commit()
            conn.close()

            ui.notify("User " + name + " erstellt")
            dialog.close()
            ui.navigate.to("/")
    else:
        ui.notify("Der Benutzername muss mindestens 3 Zeichen lang sein")