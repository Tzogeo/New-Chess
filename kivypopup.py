from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from random import shuffle


def show_popup(header,message):
    global popup
    layout = BoxLayout(orientation='vertical')
    popup_label = Label(text=message,text_size=(300,None),color=(0.7,0.7,0.5,1))
    close_button = Button(text='OK',background_color=(0.3,0.3,0.5,1),color=(1,1,1,1),size_hint=(0.5, 0.5))
    layout.add_widget(popup_label)
    layout.add_widget(close_button)   
    popup = Popup(title=header, content=layout, size_hint=(None, None), size=(600, 600))
    close_button.bind(on_release=callback)    
    popup.open()

def callback(button_instance):
    global popup
    popup.dismiss()
    

class QuestionPopup(Widget):
    def show_question_popup(self, question: str, correct_answer: str, wrong_answers: list, callback):
        def on_answer_selected(instance: Button):
            if instance.text == correct_answer:
                callback(True)
            else:
                callback(False)
            popup.dismiss()

        answers = [correct_answer] + wrong_answers
        shuffle(answers)
        question=question.replace("&quot;",'"')
        layout = BoxLayout(orientation='vertical', spacing=10)
        question_label = Label(text=question, text_size=(300,None),halign='center', valign='middle',color=(0.7,0.7,0.5,1), size_hint_y=None, height=50)
        layout.add_widget(question_label)

        for answer in answers:
            answer_button = Button(text=answer, size_hint_y=None, height=40,background_color=(0.3,0.3,0.5,1))
            answer_button.bind(on_release=on_answer_selected)
            layout.add_widget(answer_button)

        popup = Popup(title='You got another chance.Pick the correct answer and you play again', content=layout, size_hint=(0.8, 0.5), auto_dismiss=False)
        popup.open()

