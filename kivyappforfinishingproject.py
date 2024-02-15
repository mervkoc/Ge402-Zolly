# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 20:32:37 2024

@author: HP
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy_garden.mapview import MapView, MapMarkerPopup
from google.cloud import firestore
import threading
from google.oauth2 import service_account
from PIL import Image
import time

# Specify the path to your service account key file
service_account_path = 'C:\\Users\\HP\\anaconda3\\Lib\\site-packages\\zollyapp-6ef028f890fb.json'

# Explicitly use the service account credentials
credentials = service_account.Credentials.from_service_account_file(service_account_path)
db = firestore.Client(credentials=credentials, project=credentials.project_id)

def fetch_location_data(update_ui_callback):
    doc_ref = db.collection('your_collection').document('your_document')  # Adjust as needed

    try:
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            lat = data.get('lat', 0)
            lng = data.get('lng', 0)
            # Update the UI with the fetched data
            update_ui_callback(lat, lng)
        else:
            print('No such document!')
    except Exception as e:
        print(f'An error occurred: {e}')
        

def resize_marker_image(source_path, output_path, size=(50, 50)):
    image = Image.open(source_path)
    
    # Dynamically determine the resampling filter based on what's available
    # This approach avoids direct reference to Image.ANTIALIAS or ImageResampling
    try:
        # Pillow >= 8.0.0
        resample_filter = Image.Resampling.LANCZOS
    except AttributeError:
        try:
            # Pillow < 8.0.0 (where Image.ANTIALIAS is available)
            resample_filter = Image.LANCZOS
        except AttributeError:
            # Fallback for older Pillow versions where LANCZOS might not be available
            resample_filter = Image.NEAREST
    
    image.thumbnail(size, resample_filter)
    image.save(output_path)
    
# Use the resized image as the source for your marker
resize_marker_image("C:\\Users\\HP\\anaconda3\\Lib\\site-packages\\marker.png", "C:\\Users\\HP\\anaconda3\\Lib\\site-packages\\resized_marker.png")
# Make sure you're referencing the resized marker image
marker_source = "C:\\Users\\HP\\anaconda3\\Lib\\site-packages\\resized_marker.png"

Window.size = (350, 500)
Window.clearcolor = (0.631, 0.749, 0.647)  # Set the window background color (light gray in this example)

# Define the Kivy UI
kv = """
ScreenManager:
    LoginScreen:
    MainMenuScreen:
    LocationScreen:
    HealthScreen:
    ActivityTrackingScreen:
    SettingsScreen:
    GoalsScreen:
    AlertsScreen:
    AreasScreen:

<LoginScreen>:
    name: 'login'
            
    Label:
        text: 'Pet Tracker App'
        font_size: 42
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        color: 0.165, 0.169, 0.18
        
    BoxLayout:
        orientation: 'vertical'
        size_hint: None, None
        size: 300, 200
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}


        TextInput:
            id: username_input
            hint_text: 'Username'
            size_hint_y: None
            height: 40
        TextInput:
            id: password_input
            hint_text: 'Password'
            password: True
            size_hint_y: None
            height: 40
        Button:
            text: 'Login'
            on_release: root.login(username_input.text, password_input.text)
            background_normal: ''
            background_down: ''
            background_color: 0.165, 0.169, 0.18
            color: 0.631, 0.749, 0.647
            size_hint_y: None
            height: 40
        Label:
            id: login_status
            text: ''
            color: 0.525, 0.996, 0.396

<MainMenuScreen>:
    name: 'main_menu'
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 50

            Button:
                text: 'Settings'
                on_release: app.root.current = 'Settings'
                size_hint_x: None
                width: 100
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
            
            Button:
                text: 'Pet Tracker App'
                on_release: app.root.current = 'main_menu'
                size_hint_x: 1
                halign: 'center'
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
            
            Button:
                text: 'Logout'
                on_release: app.root.current = 'login'
                size_hint_x: None
                width: 100
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
        Button:
            text: 'Location'
            on_release: app.root.current = 'location'
            background_normal: ''
            background_down: ''
            color: 0.792, 0.961, 0.741
            background_color: 0.353, 0.353, 0.4, 0.4  
        Button:
            text: 'Health'
            on_release: app.root.current = 'health'
            background_normal: ''
            background_down: ''
            color: 0.792, 0.961, 0.741
            background_color: 0.353, 0.353, 0.4, 0.7  
        Button:
            text: 'Activity Tracking'
            on_release: app.root.current = 'activity_tracking'
            background_normal: ''
            background_down: ''
            color: 0.792, 0.961, 0.741
            background_color: 0.353, 0.353, 0.4, 1 


<LocationScreen>:
    name: 'location'
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 50

            Button:
                text: 'Settings'
                on_release: app.root.current = 'Settings'
                size_hint_x: None
                width: 100
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
            
            Button:
                text: 'Back to Main Menu'
                on_release: app.root.current = 'main_menu'
                size_hint_x: 1
                halign: 'center'
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
            
            Button:
                text: 'Logout'
                on_release: app.root.current = 'login'
                size_hint_x: None
                width: 100
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
                
        MapView:
            id:mapview
            lat: 39.87  # Set the latitude of the initial map center
            lon: 32.85  # Set the longitude of the initial map center
            zoom: 13  # Set the initial zoom level
            size_hint: 1, 0.9  # Adjust the size of the map
            

<HealthScreen>:
    name: 'health'
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 50

            Button:
                text: 'Settings'
                on_release: app.root.current = 'Settings'
                size_hint_x: None
                width: 100
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
            
            Button:
                text: 'Back to Main Menu'
                on_release: app.root.current = 'main_menu'
                size_hint_x: 1
                halign: 'center'
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
            
            Button:
                text: 'Logout'
                on_release: app.root.current = 'login'
                size_hint_x: None
                width: 100
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
        BoxLayout:
            orientation: 'vertical'
        


<ActivityTrackingScreen>:
    name: 'activity_tracking'
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 50

            Button:
                text: 'Settings'
                on_release: app.root.current = 'Settings'
                size_hint_x: None
                width: 100
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
            
            Button:
                text: 'Back to Main Menu'
                on_release: app.root.current = 'main_menu'
                size_hint_x: 1
                halign: 'center'
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
            
            Button:
                text: 'Logout'
                on_release: app.root.current = 'login'
                size_hint_x: None
                width: 100
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
        BoxLayout:
            orientation: 'vertical'
 
<SettingsScreen>:
    name: 'Settings'
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 50

            Button:
                text: 'Settings'
                on_release: app.root.current = 'Settings'
                size_hint_x: None
                width: 100
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
            
            Button:
                text: 'Back to Main Menu'
                on_release: app.root.current = 'main_menu'
                size_hint_x: 1
                halign: 'center'
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
            
            Button:
                text: 'Logout'
                on_release: app.root.current = 'login'
                size_hint_x: None
                width: 100
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
        BoxLayout:
            orientation: 'vertical'
            Button:
                text: 'Safe Areas'
                on_release: app.root.current = 'safe_areas'
                background_normal: ''
                background_down: ''
                color: 0.353, 0.353, 0.4
                background_color: 1,1,1, 0.6  
            Button:
                text: 'Alerts / Notifications'
                on_release: app.root.current = 'alerts'
                background_normal: ''
                background_down: ''
                color: 0.353, 0.353, 0.4
                background_color: 1,1,1, 0.4  
            Button:
                text: 'Daily Goals'
                on_release: app.root.current = 'daily_goals'
                background_normal: ''
                background_down: ''
                color: 0.353, 0.353, 0.4
                background_color: 1,1,1, 0.2
            
                
            
            
<GoalsScreen>:
    name: 'daily_goals'
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 50

            Button:
                text: 'Settings'
                on_release: app.root.current = 'Settings'
                size_hint_x: None
                width: 100
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
            
            Button:
                text: 'Back to Main Menu'
                on_release: app.root.current = 'main_menu'
                size_hint_x: 1
                halign: 'center'
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
            
            Button:
                text: 'Logout'
                on_release: app.root.current = 'login'
                size_hint_x: None
                width: 100
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
        BoxLayout:
            orientation: 'vertical'

<AlertsScreen>:
    name: 'alerts'
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 50

            Button:
                text: 'Settings'
                on_release: app.root.current = 'Settings'
                size_hint_x: None
                width: 100
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
            
            Button:
                text: 'Back to Main Menu'
                on_release: app.root.current = 'main_menu'
                size_hint_x: 1
                halign: 'center'
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
            
            Button:
                text: 'Logout'
                on_release: app.root.current = 'login'
                size_hint_x: None
                width: 100
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
        BoxLayout:
            orientation: 'vertical'

<AreasScreen>:
    name: 'safe_areas'
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 50

            Button:
                text: 'Settings'
                on_release: app.root.current = 'Settings'
                size_hint_x: None
                width: 100
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
            
            Button:
                text: 'Back to Main Menu'
                on_release: app.root.current = 'main_menu'
                size_hint_x: 1
                halign: 'center'
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
            
            Button:
                text: 'Logout'
                on_release: app.root.current = 'login'
                size_hint_x: None
                width: 100
                background_normal: ''
                background_down: ''
                background_color: 0.165, 0.169, 0.18
                color: 0.631, 0.749, 0.647
        BoxLayout:
            orientation: 'vertical'
    
    
        
"""

# Define the Screens
class LoginScreen(Screen):
    def login(self, username, password):
        if username == 'admin' and password == 'adminpassword':
            self.manager.current = 'main_menu'
            self.ids.login_status.text = ""
            self.ids.username_input.text = ""  # Clear the username field
            self.ids.password_input.text = ""  # Clear the password field
        else:
            self.ids.login_status.text = "Incorrect username or password."
        
class MainMenuScreen(Screen):
    pass

class LocationScreen(Screen):
    marker = None  # Initialize a class variable to keep track of the current marker

    def on_enter(self, *args):
        super(LocationScreen, self).on_enter(*args)
        # Ensure any existing marker is cleared when entering the screen
        if self.marker:
            self.ids.mapview.remove_widget(self.marker)
            self.marker = None
        # Start fetching data in a separate thread
        threading.Thread(target=self.fetch_location_data_continuously, args=()).start()

    def fetch_location_data_continuously(self):
        while self.manager.current == 'location':
            # Simulate fetching new location data periodically (e.g., every few seconds)
            # Replace this with actual fetching logic as needed
            fetch_location_data(self.update_map_with_location)
            time.sleep(5)  # Adjust the sleep time as needed for your application

    def update_map_with_location(self, lat, lng):
        def ui_update(dt):
            # Clear any existing marker from the map before adding a new one
            if self.marker:
                self.ids.mapview.remove_widget(self.marker)
            
            # Create a new marker for the new location
            self.marker = MapMarkerPopup(lat=lat, lon=lng, source=marker_source)
            self.ids.mapview.add_widget(self.marker)
            
            # Center the map on the new marker
            self.ids.mapview.center_on(lat, lng)

        # Schedule the UI update to run in the main thread
        from kivy.clock import Clock
        Clock.schedule_once(ui_update)


class HealthScreen(Screen):
    pass

class ActivityTrackingScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass
class GoalsScreen(Screen):
    pass

class AlertsScreen(Screen):
    pass

class AreasScreen(Screen):
    pass


# Create the screen manager
sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(MainMenuScreen(name='main_menu'))
sm.add_widget(LocationScreen(name='location'))
sm.add_widget(HealthScreen(name='health'))
sm.add_widget(ActivityTrackingScreen(name='activity_tracking'))
sm.add_widget(SettingsScreen(name='Settings'))
sm.add_widget(GoalsScreen(name='daily_goals'))
sm.add_widget(AlertsScreen(name='alerts'))
sm.add_widget(AreasScreen(name='safe_areas'))



class MyApp(App):

    def build(self):
        return Builder.load_string(kv)
    

if __name__ == '__main__':
    MyApp().run()