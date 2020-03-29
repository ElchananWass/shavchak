import kivy
import random
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior


#global veriables that all the classes needs
soldiers_list  = []  #list of names
soldiers_pzm = {"":0,}
is_pzm = False
soldiers_time = {"":100}
stands_list = ["kitchen","s\"g"]
time_option = True  #choose between the time_lists
time_list = ["","6-10","10-14","14-18","18-22","22-2","2-6"]
time_list2 = ["","5-9","9-13","13-17","17-21","21-1","1-5"]



class MenuScreen(Screen):
    
    def __init__(self,**kawrgs):
        super().__init__(**kawrgs)
        #creating all the widgets in this screen
        b_layout = BoxLayout(orientation='vertical',spacing = 100,padding = [100,200])
        msg = "welcome to shavchak app"
        welc_label = Label(text = msg)
        bttn1 = Button(text = "table")
        bttn2 = Button(text = "soldiers")
        bttn3 = Button(text = "stands and time")
        #linking the widgets to each other
        b_layout.add_widget(welc_label)
        b_layout.add_widget(bttn1)
        b_layout.add_widget(bttn2)
        b_layout.add_widget(bttn3)
        self.add_widget(b_layout)
        #binding all the buttons
        for child in b_layout.children:
            child.bind(on_press = self.on_button_press)
        
     #function that gets called when you press a button on this screen   
     #it changes between sub-screens
    def on_button_press(self,instance):
        sm.transition.direction = 'left'
        if instance.text == "table":
            sm.current = "table"
        if instance.text == "soldiers":
            sm.current = "soldiers"
        if instance.text == "stands and time":
            sm.current = "stands"



class TableScreen(Screen):
    
    #creating widget thats need to be accessable from the class functions
    gr_layout = GridLayout(cols = len(stands_list),rows = 7)
    b_layout22 = BoxLayout(orientation = "vertical")
    if_pzm = CheckBox()
    
    def __init__(self,**kawrgs):
        super().__init__(**kawrgs)
         #creating all the widgets in this screen
        b_layout = BoxLayout(orientation='vertical',spacing = 100,padding = [100,200])
        b_layout2 = BoxLayout()  #row 2:
        b_layout21 = BoxLayout()
        b_layout3 = BoxLayout()  #row 3:
        b_layout4 = BoxLayout()  #row4:
        refresh = Button(text = "refresh")
        accept = Button(text = "accept")
        self.write_time(self.b_layout22)
        #linking the widgets to each other
        b_layout.add_widget(b_layout2)
        #row 2
        b_layout2.add_widget(b_layout21)
        b_layout21.add_widget(self.gr_layout) 
        b_layout2.add_widget(self.b_layout22) 
        #row 3
        b_layout.add_widget(b_layout3)
        b_layout3.add_widget(Label(text = "allow pzm:"))
        b_layout3.add_widget(self.if_pzm)
        #row 4
        b_layout.add_widget(b_layout4)
        b_layout4.add_widget(refresh)
        b_layout4.add_widget(accept)
        b_layout.add_widget(Button(text = "return to menu"))
        self.add_widget(b_layout)
        #binding all the buttons
        for child in b_layout.walk(restrict = True):
            if type(child) == Button:
                child.bind(on_press = self.on_button_press)
        
    #function that gets called when you press a button on this screen   
     #it manages the table on top
    def on_button_press(self,instance):
        global soldiers_time,is_pzm
        temp_time =  soldiers_time.copy()
        if instance.text == "refresh":
            is_pzm = self.if_pzm.active
            self.write_time(self.b_layout22)
            self.create_table(temp_time)
        if instance.text == "accept":
            soldiers_time = temp_time
        if instance.text =="return to menu":
            sm.transition.direction = 'right'
            sm.current = "menu"
            
    #helper func that create the table of guards
    #does not return its just add to gr_layout
    def create_table(self,temp_time):
        global stands_list,soldiers_list
        self.gr_layout.clear_widgets()
        cols =  len(stands_list)
        self.gr_layout.cols = cols
        self.kitchen = []
        for stnd in stands_list:
           self.add_to_table(stnd)
        for i in range(cols*6):
              self.add_to_table(self.get_sldr(temp_time,i,cols,self.kitchen))
              if  i % cols == 0:
                  for name in soldiers_list:
                      temp_time[name] += 4
     
    #helper func that return the next soldier for the table
    #if there isnt available soldier it returns empty
    def get_sldr(self,temp_time,i,cols,kitchen):
        global soldiers_list,is_pzm,soldiers_pzm
        random.shuffle(soldiers_list)
        for name in soldiers_list:
            a = (temp_time[name] > 8) and (name not in kitchen)
            b = (i % cols !=0) or i < cols*2
            c = True
            if is_pzm:
                c = soldiers_pzm[name] < 6
            if a and b and c:
                temp_time[name] = 0
                if i % cols == 0:
                    kitchen.append(name)
                return name
        return ""
    
    #helper function that adds a soldier 
    #to the table in gr_layout
    def add_to_table(self,string):
        self.gr_layout.add_widget(Label(text = string))
    
    #helper func that writes the time stamps 
    #next to the table
    def write_time(self,b_layout22):
        self.b_layout22.clear_widgets()
        if time_option:
            for tm in time_list:
                b_layout22.add_widget(Label(text = tm))
        else:
            for tm in time_list2:
                b_layout22.add_widget(Label(text = tm))



class SoldiersScreen(Screen):
    
    def __init__(self,**kawrgs):
        super().__init__(**kawrgs)
        #creating all the widgets in this screen
        b_layout = BoxLayout(orientation='vertical',spacing = 100,padding = [100,200])  #row 1
        msg = "here you can add or delete soldiers"
        welc_label = Label(text = msg)
        b_layout2 = BoxLayout()  #row 2
        name = TextInput(multiline = False)
        b_layout3 = BoxLayout()  #row 3
        draft_msg = Label(text="draft peroid? 1 2 3...")
        gr_layout = GridLayout(rows = 4,spacing = 10)
        b_layout4 = BoxLayout()  #row 4
        add = Button(text = "add")
        remove = Button(text = "remove")
        #linking the widgets to each other
        self.add_widget(b_layout)
        #row 1
        b_layout.add_widget(welc_label)
        #row 2
        b_layout.add_widget(b_layout2)
        b_layout2.add_widget(Label(text = "soldier name"))
        b_layout2.add_widget(name)
        #row 3
        b_layout.add_widget(b_layout3)
        b_layout3.add_widget(draft_msg)
        self.create_toggle(gr_layout)
        b_layout3.add_widget(gr_layout)
        #row 4
        b_layout.add_widget(b_layout4)
        b_layout4.add_widget(add)
        b_layout4.add_widget(remove)
        #row 5
        b_layout.add_widget(Button(text = "return to menu"))
        #binding all the buttons and texts
        name.bind(text=self.on_text)
        for child in b_layout.walk(restrict = True):
            if type(child) == Button:
                child.bind(on_press = self.on_button_press)
        
    #function that gets called when you press a button on this screen   
     #it manages the soldiers list
    def on_button_press(self,instance):
        global soldiers_time,soldiers_pzm
        sldr_name = self.sldr_name
        if instance.text == "remove":
            if sldr_name in soldiers_list:
               self.remove_soldiers(sldr_name)
        if instance.text == "add" and sldr_name != "":
           self.add_soldiers(sldr_name)
        if instance.text =="return to menu":
            sm.transition.direction = 'right'
            sm.current = "menu"
            
    #func that gets called on inputing text
    #it sets the name of the soldier
    def on_text(self,instance,value):
        self.sldr_name = value
        
    #helper func that gets a name and
    #remove it from all the places
    def remove_soldiers(self,sldr_name):
        soldiers_list.remove(sldr_name)
        soldiers_time.pop(sldr_name)
        soldiers_pzm.pop(sldr_name)
    
    #helper func that gets a soldier name and
    #adds it to all the relevent places
    def add_soldiers(self,sldr_name):
        soldiers_list.append(sldr_name)
        soldiers_time[sldr_name] = 9
        for tggle in ToggleButtonBehavior.get_widgets('period'):
            if tggle.state == "down":
                soldiers_pzm[sldr_name] = int(tggle.text)
            else:
                soldiers_pzm[sldr_name] = 1
     
     #helper func that creat the toggle widget
    def create_toggle(self,gr_layout):
        for i in range(8):
            tg = ToggleButton(text = str(i+1),group = "period")
            gr_layout.add_widget(tg)
             
             
             
class StandsScreen(Screen):
    
    def __init__(self,**kawrgs):
        super().__init__(**kawrgs)
        #creating all the widgets in this screen
        b_layout = BoxLayout(orientation='vertical',spacing = 100,padding = [100,200])  #row 1
        self.add_widget(b_layout)
        msg = "here you can choose time schedule \n and uptade stands"
        welc_label = Label(text = msg)
        b_layout2 = BoxLayout()  #row 2
        time1 = ToggleButton(text = "6-10",group = "1")
        time2 = ToggleButton(text = "5-9",group = "1")
        b_layout3 = BoxLayout()  #row 3
        stand_name = TextInput()
        b_layout4 = BoxLayout()  #row 4
        add = Button(text = "add")
        remove = Button(text = "remove")
        #linking the widgets to each other
        #row 1
        b_layout.add_widget(welc_label)
        #row 2
        b_layout.add_widget(b_layout2) 
        b_layout2.add_widget(time1)  
        b_layout2.add_widget(time2)   
        #row 3
        b_layout.add_widget(b_layout3)
        b_layout3.add_widget(Label(text="stand name"))  
        b_layout3.add_widget(stand_name)
        #row 4
        b_layout.add_widget(b_layout4)
        b_layout4.add_widget(add)
        b_layout4.add_widget(remove)
        #row 5
        b_layout.add_widget(Button(text = "save and return to menu"))
        #binding all the buttons and texts
        stand_name.bind(text=self.on_text)
        for child in b_layout.walk(restrict = True):
            if type(child) == Button:
                child.bind(on_press = self.on_button_press)
        
    #function that gets called when you press a button on this screen   
     #it manages the stands list
    def on_button_press(self,instance):
        global stands_list,time_option
        if instance.text == "remove":
           if self.stnd_name in stands_list:
               stands_list.remove(self.stnd_name)
        if instance.text == "add":
            if self.stnd_name not in stands_list and self.stnd_name != "":
                stands_list.append(self.stnd_name)
        if instance.text =="save and return to menu":
            sm.transition.direction = 'right'
            self.set_time_option()
            sm.current = "menu"
            
    #func that gets called on inputing text
    #it sets the name of the stand
    def on_text(self,instance,value):
        self.stnd_name = value
        
    #helper func that gets the choice of the user
    #and set the time_option based on it
    def set_time_option(self):
        global time_option
        for tggle in ToggleButtonBehavior.get_widgets('1'):
               if tggle.state == "down":
                   if tggle.text == "6-10":
                       time_option = True
                   else:
                       time_option = False



#the base class that runs the app
class TestApp(App):
    def build(self):
        return sm
    
    
    
# Create the screen manager and adding the screens
sm = ScreenManager()
menu = MenuScreen(name='menu')
sm.add_widget(menu)
soldiers = SoldiersScreen(name='soldiers')
sm.add_widget(soldiers)
stands = StandsScreen(name='stands')
sm.add_widget(stands)
table = TableScreen(name='table')
sm.add_widget(table)

#running the app
if __name__ == '__main__':
    TestApp().run()