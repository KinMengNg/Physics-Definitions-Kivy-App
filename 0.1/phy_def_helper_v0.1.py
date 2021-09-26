from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import threading
import random

Builder_string = '''
ScreenManager:
    Main:
<Main>:
    name : 'Definition App'
    BoxLayout:
        orientation: "vertical"
        MDToolbar:
            title: 'Definition App'
            md_bg_color: app.theme_cls.primary_color
            specific_text_color: 1, 1, 1, 1
        MDTextField:
            id: your_query
            hint_text: "Your Query (The word you want to define)"
            color_mode: 'custom'
            helper_text_mode: "on_focus"
            markup: True
        MDTextField:
            id: your_definition
            hint_text: "Your Definition"
            color_mode: 'custom'
            helper_text_mode: "on_focus"
            markup: True

        ScrollView:
            Label:
                id: label_1
                text: 'Actual Definition (Missing words will be bolded and underlined)'
                color:'#1675f7'
                markup: True
                multiline: True
                size_hint_y: None
                size: self.texture_size
                height: self.texture_size[1]  
                text_size: self.width, None
                

        MDRectangleFlatIconButton:
            text: "Check"
            icon: "clipboard-search"
            line_color: 0, 0, 0, 0
            pos_hint: {"center_x": .5, "center_y": .6}
            on_press: app.run_fun()
        MDRectangleFlatIconButton:
            text: "Random"
            icon: "boomerang"
            line_color: 0, 0, 0, 0
            pos_hint: {"center_x": .5, "center_y": .6}
            on_press: app.random()
        MDRectangleFlatIconButton:
            text: "List All"
            icon: "view-list"
            line_color: 0, 0, 0, 0
            pos_hint: {"center_x": .5, "center_y": .6}
            on_press: app.list_all()
            
        MDSpinner:
            id: rc_spin
            size_hint: None, None
            size: dp(46), dp(46)
            pos_hint: {'center_x': .5, 'center_y': .5}
            active: False
    '''


class Main(Screen):
    pass


sm = ScreenManager()
sm.add_widget(Main(name='Definition_App'))


class MainApp(MDApp):
    def build(self):
        self.help_string = Builder.load_string(Builder_string)
        self.title = 'Definition App'
        self.definitions = {}
        with open('physics_definitions.txt') as f1:
            #each line should have 1 definition, tab seperated
            for line in f1:
                word, definition = line.strip().split('\t')
                self.definitions[word] = definition

        return self.help_string

    def run_fun(self):
        t1 = threading.Thread(target=self.search)
        t1.start()

    def random(self):
        random_query, definition = random.choice(list(self.definitions.items()))
        self.help_string.get_screen('Definition App').ids.your_query.text = random_query

    def list_all(self):
        full_text = ''
        self.help_string.get_screen('Definition App').ids.rc_spin.active = True
        for word in self.definitions:
            definition = self.definitions[word]
            full_text += f'[b]{word}[/b]:  {definition}\n\n'
            
        self.help_string.get_screen('Definition App').ids.label_1.text = full_text
        self.help_string.get_screen('Definition App').ids.rc_spin.active = False    
        
    def search(self):
        self.help_string.get_screen('Definition App').ids.rc_spin.active = True
        query = self.help_string.get_screen('Definition App').ids.your_query.text
        user_definition = self.help_string.get_screen('Definition App').ids.your_definition.text
        result = self.get_result(query, user_definition)
##        result = wikipedia.summary(query, sentences=6)
        result = result.strip()
        self.help_string.get_screen('Definition App').ids.label_1.text = result
        self.help_string.get_screen('Definition App').ids.rc_spin.active = False

    #function to help underline words i missed later on
    def underline(self, string):
##        emptystring = ''
##
##        for i in range(0, len(string)):
##
##            if string[i] == ' ':
##                emptystring = emptystring + string[i]
##            else:
##                emptystring= emptystring+string[i]+str('̲') #'\u0332'
##
##        #return emptystring

        #have to redefine cause kivy dont know underline unicode
        return '[b][u]'+string+'[/u][/b]'

    def get_result(self, query, user_definition):
        exist = False
        #get actual definition
        query = query.lower()
        if query in self.definitions:
            exist = True
            actual_definition = self.definitions[query]
        else:
            return 'I do not know the definition to the word you tried to define, did you spell it correctly? Or try phrasing it differently.'

        if exist == True:
            #get each individual word, so i can see which words i missed
            actual_definition_words = actual_definition.strip().split(' ') #this is for compare
            output_definition_words = actual_definition_words.copy() #this is my backup copy
            user_answer_words = user_definition.strip().split(' ')

            #compare
            for word in user_answer_words:
                word = word.lower()
                if (word in actual_definition_words):
                    actual_definition_words.remove(word) #remove the word

                #sometimes the word is connected to the comma, full stop, or without it
                elif (word+',') in actual_definition_words:
                    actual_definition_words.remove(word+',')

                elif (word+'.') in actual_definition_words:
                    actual_definition_words.remove(word+'.')

                elif (word[:-1]) in actual_definition_words:
                    actual_definition_words.remove(word[:-1])



            output = ''

            for word in output_definition_words:
                #if its in that list, means did not mention, so underline
                if (word in actual_definition_words) and (word not in ['an', 'the', 'of', 'is', 'it', 'a', 'to', 'at', 'are', 'that']):
                    word = self.underline(word)

                output += word + ' '
            return output

    
MainApp().run()
