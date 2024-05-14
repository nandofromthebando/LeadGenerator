from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

#Popups from other project refer to documentation.


class CustomPopup(Popup):
    def __init__(self, title, message, **kwargs):
        super().__init__(**kwargs)

        # For info popups
        self.title = title
        self.size_hint = (None, None)
        self.size = (800, 400)
        self.background_color = (0.8, 0.8, 0.8, 1)  # Set background color to light gray
        self.separator_color = (1, 1, 1, 1)  # Set separator color to dark gray
        self.auto_dismiss = True  # Prevent dismissing when clicking outside the popup

        # Add message label
        self.message_label = Label(
            text=message,
            size_hint=(1, None),
            height=150,
            font_size='16sp',
            color=(1, 1, 1, 1)  # Set text color to dark gray
        )

        # Add close button
        self.close_button = Button(
            text="Close",
            size_hint=(None, None),
            size=(100, 50),
            font_size='16sp',
            background_color=(0.2, 0.6, 0.2, 1),  # Set button color to green
            color=(1, 1, 1, 1)  # Set button text color to white
        )
        self.close_button.bind(on_press=self.dismiss)

        # Layout setup
        self.layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(1, None))
        self.layout.add_widget(self.message_label)
        self.layout.add_widget(self.close_button)

        self.content = self.layout



class AnalyzePopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set popup properties
        self.title = "Please Name and Specify File Type"
        self.size_hint = (None, None)
        self.size = (800, 400)
        self.background_color = (0.8, 0.8, 0.8, 1)  # Set background color to light gray
        self.separator_color = (1, 1, 1, 1)  # Set separator color to dark gray
        self.auto_dismiss = True  # Prevent dismissing when clicking outside the popup

        # Initialize variables to store user input
        self.selected_file_type = None
        self.filename = None

        # Add message label
        self.message_label = Label(
            text="Input Name and File Type:",
            size_hint=(1, None),
            height=150,
            font_size='16sp',
            color=(1, 1, 1, 1)  # Set text color to dark gray
        )

        # Add dropdown menu for file type selection
        self.file_type_dropdown = DropDown()
        file_types = ['CSV', 'XML', 'XLS']
        for file_type in file_types:
            btn = Button(text=file_type, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.select_file_type(btn.text))
            self.file_type_dropdown.add_widget(btn)

        self.file_type_button = Button(text='Select File Type', size_hint=(None, None), size=(150, 50))
        self.file_type_button.bind(on_release=self.file_type_dropdown.open)
        self.file_type_dropdown.bind(on_select=self.update_file_type)

        # Add close button
        self.save_button = Button(
            text="Save",
            size_hint=(None, None),
            size=(100, 50),
            font_size='16sp',
            background_color=(0.2, 0.6, 0.2, 1),  # Set button color to green
            color=(1, 1, 1, 1),  # Set button text color to white
            on_press=self.save_and_dismiss
        )

        # Add close button
        self.cancel_button = Button(
            text="Cancel",
            size_hint=(None, None),
            size=(100, 50),
            font_size='16sp',
            background_color=(0.2, 0.6, 0.2, 1),  # Set button color to green
            color=(1, 1, 1, 1),  # Set button text color to white
            on_press=self.dismiss
        )

        # User input the file name
        self.analyze_file_entry = TextInput(text='', font_size='16sp', background_color=(0.3, 0.3, 0.3, 1), size_hint_y=None, height=40)
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

class Sites_to_Scrape(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set popup properties
        self.title = "News Websites List"
        self.size_hint = (None, None)
        self.size = (800, 600)
        self.background_color = (0.8, 0.8, 0.8, 1)  # Set background color to light gray
        self.separator_color = (1, 1, 1, 1)  # Set separator color to dark gray
        self.auto_dismiss = True  # Prevent dismissing when clicking outside the popup

        # Create a grid layout for labels
        grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Add labels for each news website link
        news_sites = [
            "https://www.bbc.com/news",
            "https://www.nytimes.com/",
            "https://edition.cnn.com/",
            "https://www.theguardian.com/international",
            "https://www.foxnews.com/",
            "https://www.nbcnews.com/",
            "https://www.washingtonpost.com/",
            "https://www.usatoday.com/",
            "https://www.reuters.com/",
            "https://www.bloomberg.com/",
            "https://www.aljazeera.com/",
            "https://www.huffpost.com/",
            "https://www.buzzfeednews.com/",
            "https://www.independent.co.uk/",
            "https://www.euronews.com/",
            "https://apnews.com/",
            "https://www.rte.ie/news/",
            "https://timesofindia.indiatimes.com/",
            "https://www.hindustantimes.com/",
            "https://www.dawn.com/",
        ]
        # Add message label
        self.message_label = Label(
            text="Here is a list of common websites:",
            size_hint=(1, None),
            height=150,
            font_size='26sp',
            color=(1, 1, 1, 1)  # Set text color to dark gray
        )

        # Create a grid layout for labels
        grid_layout = GridLayout(cols=2, spacing=20, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        
        for site in news_sites:
            label = Label(text=site, font_size='18sp', color=(1, 1, 1, 1), halign='center', valign='middle')
            grid_layout.add_widget(label)
            
        # Create a scroll view to contain the grid layout
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(grid_layout)

        # Add close button
        self.close_button = Button(
            text="Close",
            size_hint=(None, None),
            size=(100, 50),
            font_size='16sp',
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

