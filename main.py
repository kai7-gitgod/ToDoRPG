from nicegui import ui
import home_page
import pages.user_homepage
import pages.edit_questpage
import pages.closed_questpage
import pages.create_questpage

home_page.createDatabase()

ui.run()
