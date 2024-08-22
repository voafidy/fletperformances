 
import sqlite3
import string
from flet import *

class LoginForm(UserControl):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success

    def build(self):
        self.titre_app = Text("Performance Plus - Management System", size=25, color="#081d33")
        self.username = TextField(label="Identifiant", bgcolor='gray', width=300)
        self.password = TextField(label="Mot-de-passe", password=True, bgcolor='gray',can_reveal_password=True, width=300)
        self.error_message = Text("", color=colors.RED)
        self.message_login = Text("Connectez-vous pour travailler", color=colors.BLACK, size=15)
        self.message_csi = Text("Si vous avez des questions, n'hésitez pas à nous contacter : Cratol Service Informatique Tél.  037 27 884 67", color=colors.BLACK, size=10)

        def close_window(e):
            self.page.window_close()

        return Container(
            alignment=alignment.center,
            content=Container(
                bgcolor='#b0f2b6',
                padding=20,
                border_radius=10,
                content=Column(
                    controls=[
                        self.titre_app,
                        Divider(height=2, color="transparent"),
                        self.message_login,
                        self.username,
                        self.password,
                        self.error_message,
                        Row(
                            controls=[
                                ElevatedButton(
                                    on_click=self.handle_login,
                                    bgcolor='#081d33',
                                    color='white',
                                    content=Text(
                                        'Connexion',
                                        size=13,
                                        weight='bold',
                                    ),
                                    style=ButtonStyle(
                                        shape={
                                            "": RoundedRectangleBorder(radius=6),
                                        },
                                        color={
                                            "": "white",
                                        },
                                    ),
                                    height=37,
                                    width=120,
                                ),
                                ElevatedButton(
                                    on_click=close_window,
                                    bgcolor='#081d33',
                                    color='white',
                                    content=Text(
                                        'Quitter',
                                        size=13,
                                        weight='bold',
                                    ),
                                    style=ButtonStyle(
                                        shape={
                                            "": RoundedRectangleBorder(radius=6),
                                        },
                                        color={
                                            "": "white",
                                        },
                                    ),
                                    height=37,
                                    width=120,
                                ),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            spacing=10
                        ),
                        Divider(height=3, color="transparent"),
                        self.message_csi
                    ],
                    horizontal_alignment="center",
                    alignment=MainAxisAlignment.CENTER,
                    spacing=10
                ),
                width=600,
                height=360,
            ),
            
        )




    #"pour le lminiscule ou majuscule"
    alphabets_upper = string.ascii_uppercase
    alphabets_lower = string.ascii_lowercase
    def close_window(self,e):
            self.page.window_close()
            
    def connect_to_db():
        connection = sqlite3.connect('https://u.pcloud.link/publink/show?code=XZbN7O0ZwjB5uniXk34UNf98RUzme0LB7Ry7')  # Remplacez par l'URL de votre base de données
        cursor = connection.cursor()
        return cursor, connection
    def load_data_login(self,identifiant,mdp):
        # Charger les données existantes pour l'enregistrement à modifier
        conn = sqlite3.connect('BDD/database.db')                                                                                                                                         
        cur = conn.cursor()
        cur.execute("SELECT * FROM loginTb WHERE identifiant = ? AND mdp=?", ("Bota","bota"))
        #cur.execute("SELECT * FROM loginTb WHERE identifiant = ? AND mdp=?", (identifiant,mdp))
        self.data = cur.fetchone()
        conn.close()
      
    def handle_login(self, e):
        self.load_data_login(self.username.value,self.password.value)
        print(self.username.value)
        print(self.password.value)
        # Dummy authentication logic
        if self.data:
            check_login=1
            self.on_login_success(self.data[1],self.data[3],self.data[4])
            '''
            if 'm' == "m" and 'v' == "v":
                self.on_login_success(self.username.value)
            '''
        else:
            check_login=0
            self.error_message.value = "Oops! Identifiant ou Mot de passe incorrecte..."
            self.error_message.update()
        return check_login


import flet
from flet import *
from form_setting import AppSetting
from header import AppHeader
from form import AppForm
from data_table import AppDataTable
from caisse_form import CaisseForm
from login_form import LoginForm  # Import the LoginForm
from screeninfo import get_monitors

from stat_form import StatForm

def main(page: Page):
    page.title = "Performance Plus-CSI"
    page.bgcolor = '#fdfdfd'
    page.padding = 8
    page.window.bgcolor = colors.TRANSPARENT
    page.bgcolor =colors.TRANSPARENT
    #page.window.title_bar_hidden = True
    #page.window.frameless = True
    page.window_maximized = True
    # Recalculate the center position

    content_column = Column(expand=True)
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    def on_login_success(username, nom, statut):
        page.controls.clear()
        content_column.controls.clear()
        content_column.controls.append(
            Column(
                expand=True,
                controls=[
                    AppForm(username),
                    Column(
                        scroll='auto',
                        expand=True,
                        controls=[
                            AppDataTable(username,current_date,current_date)
                        ]
                    )
                    #StatForm(page,username)
                    #AppSetting(page),
                    #CaisseForm(page,username),
                    
                    
                ]
            )
        )
        page.add(
            Column(
                expand=True,
                controls=[
                    AppHeader(page, content_column, username, nom, statut, on_logout),
                    Divider(height=2, color="transparent"),
                    content_column
                ]
            )
        )
        page.window_maximized = True
        page.bgcolor ='#fdfdfd'
        page.window.title_bar_hidden = False
        page.window.frameless = False
        page.update()

    def on_logout():
        page.controls.clear()
        login_form = LoginForm(on_login_success)
        page.add(login_form)
        page.window_maximized = True
        page.window.bgcolor = colors.TRANSPARENT
        page.bgcolor =colors.TRANSPARENT
        page.window.title_bar_hidden = True
        page.window.frameless = True
        page.update()

    login_form = LoginForm(on_login_success)
    page.add(login_form)
    page.update()

if __name__ == "__main__":
    #flet.app(target=main)
    flet.app(target=main, view=AppView.WEB_BROWSER,host="localhost",port=5050)
    
#flet main.py -d
'''AppForm(username),
                    Column(
                        scroll='auto',
                        expand=True,
                        controls=[
                            AppDataTable(username,current_date,current_date)
                        ]
                    )'''
                    
                    
                    
