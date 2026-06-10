import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout  
from kivy.uix.textinput import TextInput 
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
import socket
kivy.require("2.3.1")
host = '172.29.19.197'
port = 63635
address = (host,port)
def sev_connect():
    client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    return client

# cypher password
def encrption(passord ,key):
    alphabeta ={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7,"i":8
                ,"j":9,"k":10,"l":11,"m":12,"n":13,"o":14,"p":15,"q":16,"r":17
                ,"s":18,"t":19,"u":20,"v":21,"w":22,"x":23,"y":24,"z":25,"@":26,"#":27,
                "1":28,"2":29,"3":30,"4":31,"5":32,"6":33,"7":34,"8":35,"9":36,"0":37}
    alphabeta_list =["a","b","c","d","e","f","g","h","i"
                ,"j","k","l","m","n","o","p","q","r"
                ,"s","t","u","v","w","x","y","z","@","#",
                "0","1","2","3","4","5","6","7","8","9"]
    passord_after = ""
    for x in passord:
        new_key = alphabeta[x] - key
        passord_after = passord_after+alphabeta_list[new_key]
    return passord_after

def is_up():
    client = sev_connect()
    msg = "syn"
    client.sendto(bytes(msg,"utf-8"),address)
    msg = client.recvfrom(4096)
    msg = msg[0].decode("utf-8")
    if msg :
        print(msg)
    return client

class Main(App):
    def build(self):
        self.manger = ScreenManager()
        #=====================================
        self.log = login_page()
        screen = Screen(name="login")
        screen.add_widget(self.log)
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
        user = self.user.text
        passcode =self.passcode.text
        Clock.schedule_once(self.connect, 1)

    def sign_up_button(self, instance):
        App_main.manger.current ="sign_up"

    def connect(self,_):
        try:
            client = sev_connect()
            msg = "check"
            client.sendto(bytes(msg,"utf-8"),address)
            data = f"{self.user.text}:{self.passcode.text}"
            client.sendto(bytes(data,"utf-8"),address)
            msg = client.recvfrom(4096)
            msg = msg[0].decode("utf-8")
            print(msg)
            if msg == "found":
                S_C = client.recvfrom(4096)
                S_C = S_C[0].decode("utf-8")
                Cookie = S_C.split("++")
                role = Cookie[0]
                id = Cookie[1]
                App_main.welcome.status(role)
                App_main.manger.current ="welcome"
                
            else:
                App_main.manger.current ="login"
        except Exception as e:
            print(e)
            pass
        finally:
            client.close()

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
        btn2.bind(on_press=self.sign_out)
        top_bar.add_widget(title)
        top_bar.add_widget(spacer)
        top_bar.add_widget(btn2)
        
        # Main content area
        content = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.status_is = Label(text=f'ahhhhhh', font_size=20)
        content.add_widget(self.status_is)
        
        
        # Add everything to main layout
        layout.add_widget(top_bar)
        layout.add_widget(content)
        
        self.add_widget(layout)
    def sign_out(self ,instance):
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
    def back_in(self, instance):
        App_main.manger.current ="login"
    
    def connect(self,_):
        try:
            client = sev_connect()
            msg = "create"
            client.sendto(bytes(msg,"utf-8"),address)
            data = f"{self.user.text}:{self.passcode.text}:{self.main_button.text.strip()}"
            client.sendto(bytes(data,"utf-8"),address)
            msg = client.recvfrom(4096)
            msg = msg[0].decode("utf-8")
            if msg == "found":
                App_main.manger.current ="sign_up"
                print(msg)
            elif msg == "done":
                S_C = client.recvfrom(4096)
                S_C = S_C[0].decode("utf-8")
                App_main.manger.current ="welcome"
        except Exception as e:
            print(e)
            pass
        finally:
            client.close()

if __name__ == "__main__":
    try:
        App_main = Main()
        App_main.run()
    except Exception as e:
        print(e)
        pass