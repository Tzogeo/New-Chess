from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

def show_popup(header,message):
    layout = BoxLayout(orientation='vertical')
    popup_label = Label(text=message,text_size=(300,None))
    close_button = Button(text='OK',background_color=(0.5,0.5,0.5,1),color=(1,1,1,1),size_hint=(None, None), size=(40, 40))
    layout.add_widget(popup_label)
    layout.add_widget(close_button)
    
    popup = Popup(title=header, content=layout, size_hint=(None, None), size=(400, 400))
    close_button.bind(on_release=popup.dismiss)
    popup.open()
