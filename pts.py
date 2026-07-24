import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from kivy.uix.textinput import TextInput 
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from requests import Session
session_connection = Session()
kivy.require("2.3.1")


class Scrollable_dashboard(ScrollView):
    session_number = []
    for_student = []
    name = []
    sessions = []
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_scroll_x = False
    def build(self):
        rows  = self.update_chat_history()
        main_layout = BoxLayout(orientation='vertical',  spacing=10,size_hint_y=None,height=self.calculate_height())

        for i  in range(len(rows)):
            row = BoxLayout(orientation='horizontal', spacing=10, padding=10)
            name = Label(size_hint_y=None,height=50)
            name.text = rows[i][0]
            row.add_widget(name)

            session_number = Label(size_hint_y=None,height=50)
            session_number.text = rows[i][1]
            row.add_widget(session_number)
            
            for_student = Label(size_hint_y=None,height=50)
            for_student.text = rows[i][2]
            row.add_widget(for_student)
            main_layout.add_widget(row)
        self.add_widget(main_layout)

    def update_chat_history(self):
        try:
            response = session_connection.get(url="http://127.0.0.1:8000/courses")
            L_of_object = []
            response = response.content.decode().replace("[","").replace("]","").replace("{","").replace("}","").replace('"',"").split(',')
            for session in response:
                filtered_req =session.split(':')
                L_of_object.append(filtered_req)

            session_number = []
            for_student = []
            name = []
            

            for i in range(len(L_of_object)):
                if L_of_object[i][0] == "session_number":
                    session_number.append(L_of_object[i][1])
                elif L_of_object[i][0] == "for_student":
                    for_student.append(L_of_object[i][1])
                elif L_of_object[i][0] == "name":
                    name.append(L_of_object[i][1])

            if not self.sessions:
                try:
                    for i in range(len(name)):

                        w = [name[i],session_number[i],for_student[i]]
                        self.sessions.append(w)
                except Exception as e:
                    App_main.the_error.error(e)
                    App_main.manger.current = "error_screen"
                finally:
                    self.session_number = session_number
                    self.for_student = for_student
                    self.name = name
            else:
                if  (session_number[-1] != self.session_number[-1] ):
                    i = len(self.sessions) + 1
                    w = [name[i],session_number[i],for_student[i]]
                    self.sessions.append(w)
            return self.sessions
        except Exception as e:
            App_main.the_error.error(e)
            App_main.manger.current = "error_screen"
    def calculate_height(self):
        # items × 50px each + 9 spacing gaps × 10px = 590px
        return len(self.update_chat_history()) * 50 + 10 *10


class login_page(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        #========================================
        self.add_widget(Label(text="username"))
        self.user = TextInput(multiline=False)
        self.add_widget(self.user)
        #========================================
        self.add_widget(Label(text="passcode"))
        self.passcode = TextInput(multiline=False)
        self.add_widget(self.passcode)
        #========================================
        self.sign_up = Button(text="sgin up")
        self.sign_up.bind(on_press=self.sign_up_button)
        self.add_widget(self.sign_up)
        #========================================
        self.log_in = Button(text="log in")
        self.log_in.bind(on_press=self.log_button)
        self.add_widget(self.log_in)

    def log_button(self, instance):
        if self.user.text and self.passcode.text:
            Clock.schedule_once(self.connect, 1)

    def sign_up_button(self, instance):
        App_main.manger.current ="sign_up"

    def connect(self,_):
        try:    
            data= {
                "username":self.user.text,
                "passcode":self.passcode.text
            }
            response =  session_connection.post(url="http://127.0.0.1:8000/login",json=data)
            if "loged in" in str(response.content): 
                if "Parant" in str(response.content):
                    App_main.welcome.status("Parant")
                elif "Student" in str(response.content):
                    App_main.welcome.status("Student")
                else:
                    App_main.welcome.status("undefind")
                App_main.welcome.history.build()
                App_main.manger.current ="welcome"

            print(response.content)

        except Exception as e:
            App_main.the_error.error(str(e))#"call the technical support"
            App_main.manger.current ="error_screen"

class welcome(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Main layout
        layout = BoxLayout(orientation='vertical')
        # === Simple Top Bar ===
        top_bar = BoxLayout(
            size_hint_y=None, 
            height=60, 
            padding=10, 
            spacing=10
            # dark blue background
        )
        
        title = Label(
            text='Dragonex',
            font_size=24,
            bold=True,
            color=(1, 1, 1, 1)
        )
        
        spacer = Label()  # pushes buttons to the right
        btn2 = Button(text='sign out', size_hint_x=None, width=100)
        self.status_is = Label(text=f'ahhhhhh', font_size=20)
        btn2.bind(on_press=self.sign_out)
        top_bar.add_widget(title)
        top_bar.add_widget(spacer)
        top_bar.add_widget(self.status_is)
        top_bar.add_widget(btn2)
        
        """# Main content area
        
        self.status_is = Label(text=f'ahhhhhh', font_size=20)
        content.add_widget(self.status_is)"""
        
        
        # Add everything to main layout
        layout.add_widget(top_bar)
        """layout.add_widget(content)"""
        self.history = Scrollable_dashboard(height=Window.size[1]*0.9, size_hint_y=None)
        layout.add_widget(self.history)

        self.add_widget(layout)

    def sign_out(self ,_):
        self.history.clear_widgets()
        App_main.manger.current ="login"

    def status(self,state="none"):
        self.status_is.text = f"you are {state}"
        
class sign_up(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        #========================================
        self.add_widget(Label(text="username"))
        self.user = TextInput(multiline=False)
        self.add_widget(self.user)
        #========================================
        self.add_widget(Label(text="passcode"))
        self.passcode = TextInput(multiline=False)
        self.add_widget(self.passcode)
        #========================================
        self.main_button = Button(          
            text="Select an Option",
            size_hint_y=None,
            height=50
        )
        options = ["Parant", "Student"]

        self.dropdown = DropDown()
        for op in options:
            btn = Button(text=op, size_hint_y=None, height=44)
            btn.bind(on_press=self.on_data_selection)
            self.dropdown.add_widget(btn)

        self.main_button.bind(on_release=self.dropdown.open)
        self.add_widget(self.main_button)
        self.store_dropdown = self.dropdown
        #========================================
        self.add_widget(Label())
        self.back_in_V = Button(text="Back")
        self.back_in_V.bind(on_press=self.back_in)
        self.add_widget(self.back_in_V)
        #========================================
        self.log_in = Button(text="log in")
        self.log_in.bind(on_press=self.log_button)
        self.add_widget(self.log_in)
        
    def log_button(self, instance):
        selected_option = self.main_button.text.strip()   

        if selected_option == "Select an Option":
            print("Please select an option!")
            # You can also show a popup here later
            return
        Clock.schedule_once(self.connect, 1)
    def on_data_selection(self, instance):
        """Handle data type selection"""
        self.selected_data_type = instance.text
        self.main_button.text = instance.text
        self.store_dropdown.dismiss()
    def back_in(self, _):
        App_main.manger.current ="login"
    
    def connect(self,_):
        try:
            data= {
                "username":self.user.text,
                "passcode":self.passcode.text,
                "rights":self.main_button.text,
            }
            response =  session_connection.post(url="http://127.0.0.1:8000/signup",json=data)
            print(response.content)
            if "Done" in str(response.content):
                if "Parant" in str(response.content):
                    App_main.welcome.status("Parant")
                    App_main.manger.current ="welcome"
                elif "Student" in str(response.content):
                    App_main.welcome.status("Student")
                    App_main.manger.current ="welcome"
                else:
                    App_main.welcome.status("undefind")
                    App_main.manger.current ="welcome"

        except Exception as e:
            print(e)
            App_main.the_error.error("call the technical support")
            App_main.manger.current ="error_screen"


class the_error(Screen,GridLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.cols = 1
        self.status_is = Label(text=f'nothing', font_size=20)
        self.add_widget(self.status_is)
    def error(self,state="none"):
        self.status_is.text = f"{state}"

class Main(App):
    def build(self):
        self.manger = ScreenManager()
        #=====================================
        self.log = login_page()
        screen = Screen(name="login")
        screen.add_widget(self.log)
        self.manger.add_widget(screen)
         #=====================================
        self.the_error = the_error()
        screen = Screen(name= "error_screen")
        screen.add_widget(self.the_error)
        self.manger.add_widget(screen)
        #=====================================
        self.welcome = welcome()
        screen = Screen(name= "welcome")
        screen.add_widget(self.welcome)
        self.manger.add_widget(screen)
        #=====================================
        self.sign_up = sign_up()
        screen = Screen(name= "sign_up")
        screen.add_widget(self.sign_up)
        self.manger.add_widget(screen)
        
        return self.manger
    
if __name__ == "__main__":
    App_main = Main()
    App_main.run()
