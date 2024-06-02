from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

# Setting window size and colour

Window.clearcolor = (239/255, 288/255, 176/255, 1)

# Define colours for ui elements
LightBlue = (173/255, 216/255, 230/255, 1)
Green = (34/255, 139/255, 34/255, 1)

# Global dictionary to store answers
answers = {}
    
# Global list to keep track of the screens visited
screen_history = []

# Welcome page layout
class WelcomePage(Button):
    def __init__(self):
        super().__init__()
        self.text = "welcome to aquaware\n(click to get started)"
        self.background_color = LightBlue
        self.color = Green
        self.bind(on_press=self.switch)

    # When button pressed, move to message 1 screen
    def switch(self, item): 
        myapp.screen_manager.current = "message1"

# Message1 layout, tells user about app
class Message1(Button):  
    def __init__(self):
        super().__init__()
        self.text = "aquaware is an app to help you\nsave water using your daily habits"
        self.background_color = LightBlue
        self.color = Green
        self.bind(on_press=self.switch)

    # when screen is tapped, move to message 2
    def switch(self, item): 
        myapp.screen_manager.current = "message2"

# Message 2 layout , tells user about the tips
class Message2(Button):  
    def __init__(self):
        super().__init__()
        self.text = "aquaware will provide personalised tips\non how you can improve your water usage"
        self.background_color = LightBlue
        self.color = Green
        self.bind(on_press=self.switch)

    # when screen is tapped, move to message 3
    def switch(self, item): 
        myapp.screen_manager.current = "message3"

# Message 3 layout, asks user to complete a survey
class Message3(Button):  
    def __init__(self):
        super().__init__()
        self.text = "please complete a survey\nso that we can estimate your water usage"
        self.background_color = LightBlue
        self.color = Green
        self.bind(on_press=self.switch)

    # when screen is tapped, move to survey
    def switch(self, item): 
        myapp.screen_manager.current = "survey1"

# Survey screens setup
class SurveyScreen(Screen): 
    def __init__(self, question, answer_key, next_screen, previous_screen, **kwargs):
        super(SurveyScreen, self).__init__(**kwargs)
        self.next_screen = next_screen
        self.previous_screen = previous_screen
        self.question = question
        self.answer_key = answer_key

        # Survey screen layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.label = Label(text=question, halign="center", valign="middle", text_size=(Window.width - 20, None), color=Green)
        self.text_input = TextInput(multiline=False, background_color=LightBlue, foreground_color=Green)
        self.error_label = Label(text="", color=(1, 0, 0, 1), halign="center", valign="middle", text_size=(Window.width - 20, None))  # Red color for errors
        self.submit_button = Button(text="Next", background_color=LightBlue, color=Green)
        self.back_button = Button(text="Back", background_color=LightBlue, color=Green)
        self.submit_button.bind(on_press=self.submit)
        self.back_button.bind(on_press=self.GoBack)
        
        # adding buttons and labels to survey screen
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.text_input)
        self.layout.add_widget(self.error_label)
        self.layout.add_widget(self.submit_button)
        self.layout.add_widget(self.back_button)
        
        self.add_widget(self.layout)


    # input validation to check if input is an interger
    def submit(self, instance):
        answer = self.text_input.text
        if not answer.isdigit():  
            self.error_label.text = "Please enter a valid number"
        else:
            self.error_label.text = ""

            # Save the answer to the global dictionary
            answers[self.answer_key] = int(answer)
            print(f"Answer: {answer}")

            # Add current screen to screen history
            screen_history.append(myapp.screen_manager.current) 
            if self.next_screen == "survey_end":
                printAnswers()
                myapp.screen_manager.get_screen("survey_end").displayUsage()
            myapp.screen_manager.current = self.next_screen
    
    # Get the last visited screen using screen history
    def GoBack(self, instance):
        if screen_history:
            previous_screen = screen_history.pop()  
            myapp.screen_manager.current = previous_screen

# Yes/No survey screen setup
class YesNoSurveyScreen(Screen): 
    def __init__(self, question, answer_key, next_screen, previous_screen, **kwargs):
        super(YesNoSurveyScreen, self).__init__(**kwargs)
        self.next_screen = next_screen
        self.previous_screen = previous_screen
        self.question = question
        self.answer_key = answer_key

        # yes/no survey screen layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.label = Label(text=question, halign="center", valign="middle", text_size=(Window.width - 20, None), color=Green)
        self.yes_button = Button(text="Yes", background_color=LightBlue, color=Green)
        self.no_button = Button(text="No", background_color=LightBlue, color=Green)
        self.back_button = Button(text="Back", background_color=LightBlue, color=Green)
        self.yes_button.bind(on_press=self.SubmitYes)
        self.no_button.bind(on_press=self.SubmitNo)
        self.back_button.bind(on_press=self.GoBack)
        
        # adding buttons to yes/no survey screen
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.yes_button)
        self.layout.add_widget(self.no_button)
        self.layout.add_widget(self.back_button)
        
        self.add_widget(self.layout)

    # call go_next_screen function when yes/no is pressed
    def SubmitYes(self, instance):
        answers[self.answer_key] = "Yes" 
        self.GoToNextScreen()

    def SubmitNo(self, instance):
        answers[self.answer_key] = "No"
        self.GoToNextScreen()
    
    def GoToNextScreen(self):

        # Add current screen to history
        screen_history.append(myapp.screen_manager.current) 

        # if next screen is end of survey, display results
        if self.next_screen == "survey_end":
            printAnswers()
            myapp.screen_manager.get_screen("survey_end").displayUsage()
        
        #move to next screen
        myapp.screen_manager.current = self.next_screen
    
    # move to last visited screen
    def GoBack(self, instance):
        if screen_history:
            previous_screen = screen_history.pop()  
            myapp.screen_manager.current = previous_screen

# Debugging and stuff REMOVE IN FINAL CODE
def printAnswers(): 
    print("Survey completed. Answers:")
    for i, (key, value) in enumerate(answers.items(), 1):
        print(f"Question {i}: {key} = {value}")


#displays water usage results screen
class ResultsScreen(Screen):

    # screen layout setup 
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.usage_label = Label(text="", halign="center", valign="middle", text_size=(Window.width - 20, None), color=Green)
        self.tips_button = Button(text="Water Saving Tips", background_color=LightBlue, color=Green)
        self.retake_survey_button = Button(text="Retake Survey", background_color=LightBlue, color=Green)
        
        # adding buttons to end screen
        self.tips_button.bind(on_press=self.displayTips)
        self.retake_survey_button.bind(on_press=self.retakeSurvey)
        self.layout.add_widget(self.usage_label)
        self.layout.add_widget(self.tips_button)
        self.layout.add_widget(self.retake_survey_button)
        self.add_widget(self.layout)

    # calculate water usage
    def displayUsage(self): 

        # water usage rates, numbers are in liters
        WaterUsageRates = {"showerUsage":7,
                           "toiletUsage":6,
                           "dishwasherUsage":20,
                           "SinkDishWashUsage":10,
                           "laundryUsage":120,
                           "teethBrushUsage":12,
                           "LawnWateringUsage":25}
        
        NumOfDays = 7
        
        # formulas for each usage source
        shower_time = answers.get("ShowerTime", 0) * (WaterUsageRates["showerUsage"]) * NumOfDays
        toilet_flushes = answers.get("ToiletFlushes", 0) * (WaterUsageRates["toiletUsage"]) * NumOfDays
        dishwasher_runs = answers.get("DishwasherRuns", 0) * (WaterUsageRates["dishwasherUsage"])
        hand_washing_dishes_time = answers.get("HandWashingDishesTime", 0) * (WaterUsageRates["SinkDishWashUsage"]) * NumOfDays
        laundry_loads = answers.get("LaundryLoads", 0) * (WaterUsageRates["laundryUsage"])
        teeth_brushing = (answers.get("TeethBrushing", 0) * (WaterUsageRates["teethBrushUsage"]) * NumOfDays 
                          if answers.get("LeaveWaterOnTeeth") == "Yes" else 0)
        lawn_watering_time = answers.get("LawnWateringTime", 0) * (WaterUsageRates["LawnWateringUsage"])
        
        total_usage = (shower_time + toilet_flushes + dishwasher_runs + hand_washing_dishes_time + 
                       laundry_loads + teeth_brushing + lawn_watering_time)

        # text displayed for water usage
        usage_text = (
            f"Weekly Water Usage:\n\n"
            f"Shower: {shower_time} litres\n"
            f"Toilet: {toilet_flushes} litres\n"
            f"Dishwasher: {dishwasher_runs} litres\n"
            f"Hand Washing Dishes: {hand_washing_dishes_time} litres\n"
            f"Laundry: {laundry_loads} litres\n"
            f"Teeth Brushing: {teeth_brushing} litres\n"
            f"Lawn watering: {lawn_watering_time} litres\n\n"
            f"Total: {total_usage} litres"
        )

        self.usage_label.text = usage_text

    # display usage tips 
    def displayTips(self, instance):
        myapp.screen_manager.get_screen("tips_screen").displayTips()
        myapp.screen_manager.current = "tips_screen"

    def retakeSurvey(self, instance):
        global answers, screen_history
        answers = {}         # Clear answers
        screen_history = []  # Clear history
        myapp.screen_manager.current = "survey1"

# displays tips for improving water usage and saving water
class TipsScreen(Screen): 
    def __init__(self, **kwargs):
        super(TipsScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # screen layout and aesthetics
        self.scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 100))
        self.tips_label = Label(text="", halign="left", valign="top", text_size=(Window.width - 20, None), color=Green)
        self.tips_label.bind(size=self.tips_label.setter('text_size'))
        
        self.back_button = Button(text="Back to Usage Statistics", size_hint=(1, None), height=50, background_color=LightBlue, color=Green)
        self.back_button.bind(on_press=self.GoBack)
        
        # adding buttons to go back
        self.scroll_view.add_widget(self.tips_label)
        
        self.layout.add_widget(self.scroll_view)
        self.layout.add_widget(self.back_button)
        self.add_widget(self.layout)
    
    # tips for water usage, if statements depend on user input
    def displayTips(self): 
        tips = []

        if answers.get("ShowerTime", 0) > 10:
            tips.append("Consider taking shorter showers to save water.")

        if answers.get("IfOwnHalfFlushButton") == "Yes":
            tips.append("Remember to use the half flush button on your toilet to save water.")

        if answers.get("DishwasherRuns", 0) > 5:
            tips.append("Try to only run the dishwasher when it's full to save water.")

        if answers.get("HandWashingDishesTime", 0) > 0:
            tips.append("When washing dishes by hand, use minimal water by only having the tap on to rinse off soap suds.")

        if answers.get("LaundryLoads", 0) > 5 or answers.get("FullLoadLaundry") == "No":
            tips.append("Only do laundry with full loads and use the cold cycle as it is more economical.")

        if answers.get("LawnWateringTime", 0) > 70:
            tips.append("Consider lowering the time spent watering your garden and do it before 10 am or after 6 pm when water is more easily absorbed by plants.")

        if not tips:
            tips.append("You have excellent water management habits. Continue your sustainable practices!")

        self.tips_label.text = "\n".join(tips)

    def GoBack(self, instance):
        myapp.screen_manager.current = "survey_end"

class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        # adds welcome page to ui
        self.welcome_page = WelcomePage()  
        screen = Screen(name="welcome")
        screen.add_widget(self.welcome_page)
        self.screen_manager.add_widget(screen)

        # adds message 1 to ui
        self.message1 = Message1()  
        screen = Screen(name="message1")
        screen.add_widget(self.message1)
        self.screen_manager.add_widget(screen)

        # adds message 2 to ui
        self.message2 = Message2()  
        screen = Screen(name="message2")
        screen.add_widget(self.message2)
        self.screen_manager.add_widget(screen)

        # adds message 3 to ui
        self.message3 = Message3()  
        screen = Screen(name="message3")
        screen.add_widget(self.message3)
        self.screen_manager.add_widget(screen)
        
        # survey questions
        questions = [
            ("1. How many minutes do you typically\nspend in the shower each day?", "ShowerTime", "survey2"),
            ("2. How many times do you flush\nthe toilet each day?", "ToiletFlushes", "survey3"),
            ("3. How many times do you run\nthe dishwasher each week?\n(if you dont own a diswasher, enter 0)", "DishwasherRuns", "survey4"),
            ("4. If washing dishes by hand,\nhow many minutes is the tap on each day?", "HandWashingDishesTime", "survey5"),
            ("5. How many loads of laundry\ndo you do each week?", "LaundryLoads", "survey6"),
            ("6. How many times do you brush your teeth each day?", "TeethBrushing", "survey7"),
            ("7. How many minutes do you spend\nwatering your lawn or garden each week?", "LawnWateringTime", "survey8")
        ]

        yes_no_questions = [
            ("8. Do you do the laundry on full loads?", "FullLoadLaundry", "survey9"),
            ("9. Does your toilet have a half flush\nand a full flush button?", "IfOwnHalfFlushButton", "survey10"),
            ("10. Do you leave the water on when brushing teeth?", "LeaveWaterOnTeeth", "survey_end")
        ]

        previous_screen = None

        # loop through questions, displaying on screen
        for i, (question, answer_key, next_screen) in enumerate(questions, 1): 
            screen = SurveyScreen(name=f"survey{i}", question=question, answer_key=answer_key, next_screen=next_screen, previous_screen=previous_screen)
            self.screen_manager.add_widget(screen)
            previous_screen = f"survey{i}"

        #loop through yes/no questions
        for i, (question, answer_key, next_screen) in enumerate(yes_no_questions, len(questions) + 1): 
            screen = YesNoSurveyScreen(name=f"survey{i}", question=question, answer_key=answer_key, next_screen=next_screen, previous_screen=previous_screen)
            self.screen_manager.add_widget(screen)
            previous_screen = f"survey{i}"

        # Add final screen
        final_screen = ResultsScreen(name="survey_end")
        self.screen_manager.add_widget(final_screen)

        # Add tips screen
        tips_screen = TipsScreen(name="tips_screen")
        self.screen_manager.add_widget(tips_screen)

        return self.screen_manager

# runs app
myapp = MyApp()  
myapp.run()
