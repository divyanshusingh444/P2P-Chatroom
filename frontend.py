from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from re import compile, search
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import client

kv = Builder.load_file("KVStyleSheet.kv")


class Popup(Popup):
    pop = ObjectProperty(None)


class Scroll(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.layout)

        self.chatview = Label(size_hint_y=None, markup=True)
        self.end = Label()
        self.layout.add_widget(self.chatview)
        self.layout.add_widget(self.end)

    def update(self, msg):
        self.chatview.text += '\n' + msg
        self.layout.height = self.chatview.texture_size[1] + 15
        self.chatview.height = self.chatview.texture_size[1]
        self.chatview.text_size = (self.chatview.width * 0.98, None)
        self.scroll_to(self.end, animate=False)




class Login(Screen):
    serverip = ObjectProperty(None)
    username = ObjectProperty(None)
    port = ObjectProperty(None)

    def join(self):
        portpattern = compile(r"^\d{1,5}$")
        serverpattern = compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        usernamepattern = compile(r"^\w{1,50}$")
        self.serverip.text = self.serverip.text.strip()
        self.port.text = self.port.text.strip()
        self.username.text = self.username.text.strip()

        if bool(search(serverpattern, self.serverip.text)) and bool(search(portpattern, self.port.text) and bool(search(usernamepattern, self.username.text))):
            if not client.getLoginInfo(self.serverip.text, int(self.port.text), self.username.text, errorConnect):
                return

            body.sm.current = 'chatpage'
            client.listenThread(body.chatpage.incomingMsg, errorConnect)
        else:

            invalid()


def errorConnect(msg):
    print(msg)
    body.ErrorPage.updateerror(body.ErrorPage, msg)
    body.sm.current = "errorpage"


class ErrorPage(Screen):

    errorline = ObjectProperty()
    txtvar = StringProperty()

    def updateerror(self, _, error):
        self.txtvar = error


def invalid():
    pop = Popup()

    pop.open()


class ChatPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.rows = 2

        self.view = Scroll(height=Window.size[1]*0.9, size_hint_y=None)
        self.add_widget(self.view)

        self.textbox = TextInput(width=Window.size[0] * 0.8, size_hint_x=None, multiline=False)
        self.send = Button(text="Send")
        self.send.bind(on_release=self.sendmsg)


        workingArea = GridLayout(cols=2)
        workingArea.add_widget(self.textbox)
        workingArea.add_widget(self.send)
        self.add_widget(workingArea)

        Window.bind(on_key_down=self.on_key_down)
        Clock.schedule_once(self.focus, 1)
        # client.listenThread(self.incomingMsg, errorConnect)

    def on_key_down(self, instance, key, code, text, _):
        if code == 40:
            self.sendmsg(None)

    def sendmsg(self, _):
        msg = self.textbox.text
        self.textbox.text = ""

        if msg:
            if msg[0:3] == "!p!":
                self.view.update(f'[color=05ddd9]{body.login.username.text}[/color] > {msg}')
            else:
                self.view.update(f'[color=dd1005]{body.login.username.text}[/color] > {msg}')
            client.sendMsg(msg)
        Clock.schedule_once(self.focus, 0.1)

    def focus(self, _):
        self.textbox.focus = True

    def incomingMsg(self, username, msg):
        self.view.update(f'[color=20dd20]{username}[/color] > {msg}')


class MyApp(App):
    def build(self):
        self.sm = ScreenManager()

        self.login = Login()
        screen = Screen(name="login")
        screen.add_widget(self.login)
        self.sm.add_widget(screen)

        self.ErrorPage = ErrorPage()
        screen = Screen(name="errorpage")
        screen.add_widget(self.ErrorPage)
        self.sm.add_widget(screen)


        self.chatpage = ChatPage()
        screen = Screen(name='chatpage')
        screen.add_widget(self.chatpage)
        self.sm.add_widget(screen)

        return self.sm


if __name__ == '__main__':
    body = MyApp()
    body.run()