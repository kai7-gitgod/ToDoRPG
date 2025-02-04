from nicegui import ui
import sqlite3
import home_page

def startUserDeletion():
    user = home_page.getUser()
    with ui.dialog(value=True).props('persistent') as dialog, ui.card():
        ui.label(("User ", user.name, " wirklich löschen?")).classes("text-lg")
        with ui.row():
            ui.button("User löschen", on_click=lambda: deleteUser(dialog), color="red", icon="delete")
            ui.button("Abbrechen", on_click=lambda: dialog.close(), color="red", icon="cancel")

def deleteUser(dialog):
    user = home_page.getUser()
    conn = sqlite3.connect("userdata.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE userid = ?", (user.userid,))

    conn.commit()
    conn.close()
    ui.notify(("User ", user.name, " erfolgreich gelöscht!"))
    dialog.close()
    ui.navigate.to("/")