import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout  
from kivy.uix.textinput import TextInput 
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
"""from kivy.uix.boxlayout import BoxLayout"""
from kivy.uix.dropdown import DropDown
from functools import partial

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

            btn = Button(size_hint_y=None,height=50)
            btn.text = "Code"
            btn.bind(on_press=partial(self.btn_QR,name.text,for_student.text))
            row.add_widget(btn)
            
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

    def btn_QR(self,name,for_student,_): 
        App_main.code_image.build(name,for_student)
        App_main.manger.current = "Code_image"
        App_main.dashboard.history.clear_widgets()

class signup_page(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        #========================================
        self.add_widget(Label(text="username",size_hint_y = None,height= 50))
        self.user = TextInput(multiline=False)
        self.user.size_hint_y = None
        self.user.height = 50
        self.add_widget(self.user)
        #========================================
        self.add_widget(Label(text="passcode",size_hint_y = None,height= 50))
        self.passcode = TextInput(multiline=False)
        self.passcode.size_hint_y = None
        self.passcode.height = 50
        self.add_widget(self.passcode)
        #========================================
        self.add_widget(Label(size_hint_y = None,height= 50))
        #========================================
        Window.bind(on_key_down=self.on_key_down)
        self.log_in = Button(text="log in",size_hint_y = None,height= 50)
        self.log_in.bind(on_press=self.log_button)
        self.add_widget(self.log_in)
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        # But we want to take an action only when Enter key is being pressed, and send a message
        if keycode == 40:
            self.log_button()
    def log_button(self, instance = None):
        if self.user.text and self.passcode.text:
            Clock.schedule_once(self.connect, 1)
    def connect(self,_):
        try:
            data= {
                "username":self.user.text,
                "passcode":self.passcode.text
            }
            response =  session_connection.post(url="http://127.0.0.1:8000/signup",json=data)
            if "Done" in str(response.content): 
                global loged_in
                loged_in = True
                App_main.dashboard.loged()
                App_main.manger.current ="dashboard"

        except Exception as e:
            print(e)
            App_main.the_error.error("call the technical support")
            App_main.manger.current ="error_screen"

class login_page(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        #========================================
        self.add_widget(Label(text="username",size_hint_y = None,height= 50))
        self.user = TextInput(multiline=False)
        self.user.size_hint_y = None
        self.user.height = 50
        self.add_widget(self.user)
        #========================================
        self.add_widget(Label(text="passcode",size_hint_y = None,height= 50))
        self.passcode = TextInput(multiline=False)
        self.passcode.size_hint_y = None
        self.passcode.height = 50
        self.add_widget(self.passcode)
        #========================================
        self.add_widget(Label(size_hint_y = None,height= 50))
        #========================================
        Window.bind(on_key_down=self.on_key_down)
        self.log_in = Button(text="log in",size_hint_y = None,height= 50)
        self.log_in.bind(on_press=self.log_button)
        self.add_widget(self.log_in)
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        # But we want to take an action only when Enter key is being pressed, and send a message
        if keycode == 40:
            self.log_button()
    def log_button(self, instance = None):
        if self.user.text and self.passcode.text:
            Clock.schedule_once(self.connect, 1)
    def connect(self,_):
        try:
            data= {
                "username":self.user.text,
                "passcode":self.passcode.text
            }
            response =  session_connection.post(url="http://127.0.0.1:8000/login",json=data)
            if "loged in" in str(response.content): 
                App_main.dashboard.history.build()
                App_main.manger.current ="dashboard"
        except Exception as e:
            print(e)
            App_main.the_error.error("call the technical support")
            App_main.manger.current ="error_screen"

class CreateSession(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        
        self.add_widget(Label(text="Enter The Name of the teacher :> ",size_hint_y=None,
            height=50))
        self.the_name = TextInput(hint_text="Name",multiline=False,size_hint_y=None,
            height=50)
        self.add_widget(self.the_name)

        self.add_widget(Label(text="Enter The Session Number of the teacher :> ",size_hint_y=None,
            height=50))
        self.the_num = TextInput(hint_text="Number",multiline=False,size_hint_y=None,
            height=50)
        self.add_widget(self.the_num)

        self.Main_dropdown = Button(
            text="Select an Option",
            size_hint_y=None,
            height=50)
        options =  ["Sec_1","Sec_2","Sec_3"]

        self.dropdown = DropDown()
        for op in options:
            btn = Button(text=op,size_hint_y=None, height=44)
            btn.bind(on_press=self.selection_box)
            self.dropdown.add_widget(btn)
        self.Main_dropdown.bind(on_release=self.dropdown.open)
        self.add_widget(self.Main_dropdown)
        self.store_dropdown = self.dropdown

        self.simple_error = Label(size_hint_y=None,height=50)
        self.add_widget(self.simple_error)

        self.add_widget(Label(size_hint_y=None,height=50))

        self.sunbmit = Button(size_hint_y=None,height=50)
        self.sunbmit.text = "Submit"
        self.sunbmit.bind(on_press=self.connect)
        self.add_widget(self.sunbmit)
    def selection_box(self ,instance):
        self.selected_data_type = instance.text
        self.Main_dropdown.text = instance.text
        self.store_dropdown.dismiss()
    def connect(self,_):
        data= {
            "name":str(self.the_name.text),
            "session_number":int(self.the_num.text),
            "for_student":str(self.selected_data_type)
        }
        resault = session_connection.post(url="http://127.0.0.1:8000/create_teacher_session",json=data)
        print(str(resault.content))
        if "complete" in str(resault.content):
            self.the_name.text = ""
            self.the_num.text = ""
            self.selected_data_type = ""
            App_main.manger.current = "dashboard"
        elif "already exist" in  str(resault.content):
            self.simple_error.text = "session number is already exist."
    
class Code_image(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
    def build(self,name:str,for_student:str):
        bar = GridLayout(cols=1)
        self.btn= Button()
        self.btn.text = "Back"
        self.btn.size_hint_max_y = 50 
        self.btn.bind(on_press=self.back_to_dashboard)
        bar.add_widget(self.btn)
        bar.size_hint_max_y = 50
        self.add_widget(bar)
        aimg = AsyncImage()
        aimg.source = "http://127.0.0.1:8000/code/?teacher=%s&&for_student=%s"%(name,for_student)
        aimg.fit_mode = "fill"
        aimg.size_hint_max_y = None
        aimg.height = Window.size[1]*0.9
        
        self.add_widget(aimg)
    def back_to_dashboard(self,_):
        self.clear_widgets()
        App_main.dashboard.history.build()
        App_main.manger.current ="dashboard"

class dashboard(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        inner_grideout = GridLayout(cols= 2)

        self.admin_linker_btn = Button()
        self.admin_linker_btn.text = "Admin linker"
        self.admin_linker_btn.height = 50
        self.admin_linker_btn.bind(on_press=self.Admin_linker)
        inner_grideout.add_widget(self.admin_linker_btn)

        self.create_session_btn = Button()
        self.create_session_btn.text = "Create Session"
        self.create_session_btn.height = 50
        self.create_session_btn.bind(on_press=self.Create_Session)
        inner_grideout.add_widget(self.create_session_btn)

        self.add_widget(inner_grideout)

        seconed_ibber_grideout = GridLayout(cols=2)

        self.signup_page_btn = Button()
        self.signup_page_btn.text = "signup page"
        self.signup_page_btn.height= 50
        self.signup_page_btn.bind(on_press=self.signup_page)
        seconed_ibber_grideout.add_widget(self.signup_page_btn)

        self.refresh_btn = Button()
        self.refresh_btn.text = "refresh page"
        self.refresh_btn.height = 50
        self.refresh_btn.bind(on_press=self.dashboard_linker)
        seconed_ibber_grideout.add_widget(self.refresh_btn)
        
        self.add_widget(seconed_ibber_grideout)
        self.history = Scrollable_dashboard(height=Window.size[1]*0.9, size_hint_y=None)
        self.add_widget(self.history)
    def dashboard_linker(self, _):
        App_main.loader.refrash()
        App_main.manger.current = "loader"
        self.history.clear_widgets()
    def Admin_linker(self ,_):
        App_main.loader.loding()
        App_main.manger.current = "loader"
        self.history.clear_widgets()
    def signup_page(self,_):
        App_main.manger.current = "signup_page"
        self.history.clear_widgets()
    def Create_Session(self,_):
        App_main.manger.current = "CreateSession"
        self.history.clear_widgets()

class loader(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text="loading"))

    def refrash(self):
        Clock.schedule_once(self.dashboard_is_loaded, 5)
    def dashboard_is_loaded(self,_):
        App_main.dashboard.history.build()
        App_main.manger.current = "dashboard"
    
    def loding(self):
        Clock.schedule_once(self.is_loaded, 5)
    def is_loaded(self,_):
        App_main.admin_linker.build()
        App_main.manger.current = "Admin_linker"
    
class Admin_linker(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.rows = 3
        global loged_in
    def build(self):
        self.teachers,self.users = self.data_from_API()
    
        self.add_widget(Label(text="Select The Name of the teacher :> ",size_hint_y=None,
        height=50))
        self.teacher_dropdown = Button(
            text="Select an Option",
            size_hint_y=None,
            height=50)
        self.dropdown_teacher = DropDown()
        for teacher in self.teachers:
            btn = Button(size_hint_y=None, height=44)
            btn.text = str(teacher)
            btn.bind(on_press=self.selection_box)
            self.dropdown_teacher.add_widget(btn)
        self.teacher_dropdown.bind(on_release=self.dropdown_teacher.open)
        self.add_widget(self.teacher_dropdown)
        self.store_dropdown = self.dropdown_teacher

        self.add_widget(Label(text="Select The Name of the teacher :> ",size_hint_y=None,
            height=50))
        #================================================================
        self.user_dropdown = Button(
            text="Select an Option",
            size_hint_y=None,
            height=50)
        self.dropdown_user = DropDown()
        for user in self.users:
            btn2 = Button(size_hint_y=None, height=44)
            btn2.text = user
            btn2.bind(on_press=self.selection_box_2)
            self.dropdown_user.add_widget(btn2)
        self.user_dropdown.bind(on_release=self.dropdown_user.open)
        self.add_widget(self.user_dropdown)
        self.store_dropdown_2 = self.dropdown_user
        #================================================================
        self.error_local = Label(size_hint_y=None,height=50)
        self.add_widget(self.error_local)
        #================================================================
        self.send_button = Button()
        self.send_button.text = "Link"
        self.send_button.size_hint_y = None
        self.send_button.height = 50
        self.send_button.bind(on_press=self.linker)
        self.add_widget(self.send_button)
    def selection_box(self ,instance):
        self.selected_data_type = instance.text
        self.teacher_dropdown.text = instance.text
        self.store_dropdown.dismiss()

    def selection_box_2(self ,instance):
        self.selected_data_type = instance.text
        self.user_dropdown.text = instance.text
        self.store_dropdown_2.dismiss()

            
    def data_from_API(self):
        try:
            response = session_connection.get(url="http://127.0.0.1:8000/all")
            
        except Exception as e:
            App_main.the_error.error(str(e))
            App_main.manger.current = "error_screen"
    
        sessions = {}
        L_of_object = []
        response = response.content.decode().replace("{","").replace("}","").strip().split("],")

        for session in response:
            
            filtered_req =session.split(":[")
            L_of_object.append(filtered_req)
        
        for i in range(len(L_of_object )):
            L_of_object[i][1] = str(L_of_object[i][1]).replace("]","").split(",")

        for i in range(len(response)):
            for j in range(len(L_of_object[i][1])):
                L_of_object[i][1][j] = L_of_object[i][1][j][1:-1]
            sessions[L_of_object[i][0][1:-2]] = L_of_object[i][1]
        """teacher : user"""
        print(sessions)
        return  sessions['teacher'],sessions['user'] 
    def linker(self, _):
        if self.teacher_dropdown.text and self.user_dropdown.text:
            params = {
                "name":self.teacher_dropdown.text,
                "username":self.user_dropdown.text,
            }
            req =session_connection.post(url="http://127.0.0.1:8000/linker",params=params)
            print(req.content)
            if ("already" in str(req.content)) or ("help" in str(req.content)):
                self.error_local.text = "this already is added"
            else:
                App_main.dashboard.history.build()
                App_main.manger.current = "dashboard"
                self.clear_widgets()

class Main(App):
    def build(self):
        self.manger = ScreenManager()
        #=====================================
        self.log = login_page()
        screen = Screen(name="login")
        screen.add_widget(self.log)
        self.manger.add_widget(screen)
        #=====================================
        self.dashboard = dashboard()
        screen = Screen(name= "dashboard")
        screen.add_widget(self.dashboard)
        self.manger.add_widget(screen)
        #=====================================
        self.the_error = the_error()
        screen = Screen(name= "error_screen")
        screen.add_widget(self.the_error)
        self.manger.add_widget(screen)
        #=====================================
        self.CreateSession = CreateSession()
        screen = Screen(name= "CreateSession")
        screen.add_widget(self.CreateSession)
        self.manger.add_widget(screen)
        #=====================================
        self.loader = loader()
        screen = Screen(name="loader")
        screen.add_widget(self.loader)
        self.manger.add_widget(screen)
        #=====================================
        self.admin_linker = Admin_linker()
        screen = Screen(name="Admin_linker")
        screen.add_widget(self.admin_linker)
        self.manger.add_widget(screen)
        #=====================================
        self.code_image = Code_image()
        screen = Screen(name="Code_image")
        screen.add_widget(self.code_image)
        self.manger.add_widget(screen)
        #=====================================
        self.signup_page = signup_page()
        screen = Screen(name="signup_page")
        screen.add_widget(self.signup_page)
        self.manger.add_widget(screen)
        return self.manger
    
class the_error(Screen,GridLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.cols = 1
        self.status_is = Label(text=f'nothing', font_size=20)
        self.add_widget(self.status_is)
    def error(self,state="none"):
        self.status_is.text = f"{state}"
if __name__ == '__main__':
    App_main = Main()
    App_main.run()