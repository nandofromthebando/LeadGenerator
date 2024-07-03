from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
import json
import pandas as pd
#Popups from other project refer to documentation.

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class CustomPopup(Popup):
    def __init__(self, title, message, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.size_hint = (None, None)
        self.size = (900, 700)
        self.auto_dismiss = True

        # Create a label for the message
        self.message_label = Label(text=message, size_hint=(1, None), height=300, halign='center', valign='middle', text_size=(self.width - 40, None))

        # Add close button
        self.close_button = Button(text="Close", size_hint=(None, None), size=(100, 50), background_color=(0.2, 0.6, 0.2, 1))
        self.close_button.bind(on_press=self.dismiss)

        # Layout setup
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.layout.add_widget(self.message_label)
        self.layout.add_widget(self.close_button)

        self.content = self.layout




class SearchPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set popup properties
        self.title = "Please Name and Specify File Type"
        self.size_hint = (None, None)
        self.size = (900, 700)
        self.background_color = (0.8, 0.8, 0.8, 1)  # Set background color to light gray
        self.auto_dismiss = True  # Prevent dismissing when clicking outside the popup

        # Initialize variables to store user input
        self.selected_file_type = None
        self.filename = None

        # Add message label
        self.message_label = Label(
            text="Input Name and File Type:\n\n\n\n",
            size_hint=(1, None),
            height=150,
            font_size='12sp',
            color=(1, 1, 1, 1)  # Set text color to dark gray
        )

        # Add dropdown menu for file type selection
        self.file_type_dropdown = DropDown()
        file_types = ['CSV', 'XML', 'XLS']
        for file_type in file_types:
            btn = Button(text=file_type, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.select_file_type(btn.text))
            self.file_type_dropdown.add_widget(btn)

        self.file_type_button = Button(text='Select File Type', size_hint=(None, None), size=(300, 50))
        self.file_type_button.bind(on_release=self.file_type_dropdown.open)
        self.file_type_dropdown.bind(on_select=self.update_file_type)

        # Add close button
        self.save_button = Button(
            text="Save",
            size_hint=(None, None),
            size=(300, 50),
            font_size='12sp',
            background_color=(0.2, 0.6, 0.2, 1),  # Set button color to green
            color=(1, 1, 1, 1),  # Set button text color to white
            on_press=self.save_and_dismiss
        )

        # Add close button
        self.cancel_button = Button(
            text="Cancel",
            size_hint=(None, None),
            size=(100, 50),
            font_size='12sp',
            background_color=(0.2, 0.6, 0.2, 1),  # Set button color to green
            color=(1, 1, 1, 1),  # Set button text color to white
            on_press=self.dismiss
        )

        # User input the file name
        self.analyze_file_entry = TextInput(text='', font_size='12sp', background_color=(0.3, 0.3, 0.3, 1), size_hint_y=None, height=40)
        self.analyze_file_entry.bind(text=self.update_filename)

        # Layout setup
        self.layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(1, None))
        self.button_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, None))
        self.layout.add_widget(self.message_label)
        self.layout.add_widget(self.analyze_file_entry)
        self.layout.add_widget(self.file_type_button)
        self.button_layout.add_widget(self.save_button)
        self.button_layout.add_widget(self.cancel_button)
        self.layout.add_widget(self.button_layout)

        self.content = self.layout

    def select_file_type(self, file_type):
        self.file_type_dropdown.select(file_type)

    def update_file_type(self, instance, file_type):
        self.selected_file_type = file_type

    def update_filename(self, instance, filename):
        self.filename = filename

    def save_and_dismiss(self, instance):
        # Check if both file type and filename are selected
        if self.selected_file_type and self.filename:
            self.dismiss((self.filename, self.selected_file_type))
        else:
            # Show an error message if either file type or filename is missing
            self.message_label.text = "Please select file type and enter filename"


        # Add close button
        self.close_button = Button(
            text="Close",
            size_hint=(None, None),
            size=(100, 50),
            font_size='12sp',
            background_color=(0.2, 0.6, 0.2, 1),  # Set button color to green
            color=(1, 1, 1, 1)  # Set button text color to white
        )
        self.close_button.bind(on_press=self.dismiss)

        # Layout setup
        self.layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(1, 1))
        self.layout.add_widget(self.message_label)
        self.layout.add_widget(scroll_view)
        self.layout.add_widget(self.close_button)

        self.content = self.layout

class BackgroundLabel(Label):
    def __init__(self, **kwargs):
        super(BackgroundLabel, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # Set the background color (R, G, B, A)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

class PreviewData(Popup):
    json_data = StringProperty()

    def __init__(self, **kwargs):
        super(PreviewData, self).__init__(**kwargs)
        self.title = "Preview of Last Scrape"
        self.size_hint = (None, None)
        self.size = (900, 700)
        self.auto_dismiss = True

        # Create a layout for the content of the popup
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Create a TextInput for file name
        self.file_input = TextInput(hint_text='Enter JSON file name', size_hint_y=None, height=50)
        self.layout.add_widget(self.file_input)

        # Create a button to load the file
        load_button = Button(text="Load File", size_hint=(1, None), height=50, background_color=(0.2, 0.6, 0.2, 1))  # Set background color to green
        load_button.bind(on_press=self.load_file)
        self.layout.add_widget(load_button)

        # Create a ScrollView to hold the Label (initially empty)
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.json_label = Label(text='', size_hint_y=None, halign='right', valign='top', text_size=(None, None)) 
        self.json_label.bind(texture_size=self.json_label.setter('size'))
        self.scroll_view.add_widget(self.json_label)
        self.layout.add_widget(self.scroll_view)

        # Add a close button
        close_button = Button(text="Close", size_hint=(1, None), height=50, background_color=(0.2, 0.6, 0.2, 1))  # Set background color to green
        close_button.bind(on_press=self.dismiss)
        self.layout.add_widget(close_button)

        self.content = self.layout

    def load_file(self, instance):
        file_name = self.file_input.text
        try:
            # Load JSON data into pandas DataFrame
            df = pd.read_json(file_name)
            # Convert DataFrame to string
            df_string = df.to_string()
            self.json_data = df_string
        except Exception as e:
            self.json_data = f"Error loading file: {str(e)}"

class PreviewLabel(ScrollView):
    def __init__(self, **kwargs):
        super(PreviewLabel, self).__init__(**kwargs)
        self.label = Label(text_size=(None, None), size_hint=(None, None), size=(800, 50))
        self.label.bind(size=self.label.setter('text_size'))
        self.add_widget(self.label)