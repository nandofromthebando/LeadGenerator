import os
import subprocess
import platform
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget  # Import Widget for separators
from kivy.core.window import Window
from kivy.uix.popup import Popup
from GUIPopups import CustomPopup , SearchPopup, CustomPopup, BackgroundLabel , PreviewData
from threading import Thread
from GoogleMapsBot import custom_google_search

class LeadGenerator(App):

    def build(self):

        # Set window size to match screen dimensions
        #Window.fullscreen = 'auto'
        # Setting background color
        Window.clearcolor = (0.133, 0.133, 0.133, 1)

        # Main layout
        root_layout = BoxLayout(orientation='vertical', size_hint=(1, None), padding=5, spacing=5)
        root_layout.bind(minimum_height=root_layout.setter('height'))

        # Align widgets vertically centered
        for child in root_layout.children:
            child.size_hint_y = None
            child.height = '60dp'  # Set fixed height
            child.pos_hint = {'center_x': 0.5}  # Center horizontally

        # Center the layout on the screen
        root_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Guide message
        welcome_message = "Welcome to Lead Generator!"
        welcome_label = BackgroundLabel(text=welcome_message, font_size='24sp', bold=True, color=(1, 1, 1, 1), size_hint=(1, None), height=60, halign='center')
        root_layout.add_widget(welcome_label)

        # Menu bar
        menu_layout = BoxLayout(size_hint=(1, None), padding=5, spacing=10)

        # Menu buttons
        menu_clear_search_button = Button(text='Clear Last Search', size_hint=(None, None), size=(250, 60), background_color =(0.2, 0.6, 0.8, 1))
        menu_clear_search_button.text_size = menu_clear_search_button.size
        menu_clear_search_button.halign = 'center'
        menu_clear_search_button.valign = 'middle'
        menu_clear_search_button.bind(on_press=self.delete_file)

        menu_preview_data_button = Button(text='Preview Data', size_hint=(None, None), size=(250, 60), background_color =(0.2, 0.6, 0.8, 1))
        menu_preview_data_button.text_size = menu_preview_data_button.size
        menu_preview_data_button.halign = 'center'
        menu_preview_data_button.valign = 'middle'
        menu_preview_data_button.bind(on_press=self.preview_data)  # Bind the method to the button press event


        menu_exit_button = Button(text='Exit', size_hint=(None, None), size=(100, 60), on_press=self.quit_app, background_color =(0.2, 0.6, 0.8, 1))
        menu_exit_button.text_size = menu_exit_button.size
        menu_exit_button.halign = 'center'
        menu_exit_button.valign = 'middle'

        status_bar = Label(text='Ready', size_hint=(1, None), height=60, color=(1, 1, 1, 1))

        menu_layout.add_widget(menu_clear_search_button)
        menu_layout.add_widget(menu_preview_data_button)
        menu_layout.add_widget(menu_exit_button)
        menu_layout.add_widget(status_bar)
        root_layout.add_widget(menu_layout)

        # Horizontal separator
        root_layout.add_widget(Widget(size_hint_y=None, height=5))

        # Add buttons to create custom popups
        start_here_button = Button(text='Start Here', size_hint=(None, None), size=(150, 60), background_color =(0.2, 0.6, 0.8, 1))
        start_here_button.bind(on_press=self.guide_message)
        features_button = Button(text='Features', size_hint=(None, None), size=(150, 60), background_color =(0.2, 0.6, 0.8, 1))
        features_button.bind(on_press=self.Features_Message)

        buttons_layout = BoxLayout(size_hint=(None, None), size=(300, 120), spacing=10)
        buttons_layout.add_widget(start_here_button)
        buttons_layout.add_widget(features_button)
        root_layout.add_widget(buttons_layout)

        sublink_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=60)
        sublink_layout.add_widget(BackgroundLabel(text='Google Map Search:', font_size='24sp', bold=True, color=(1, 1, 1, 1), size_hint=(1, None), height=60, halign='center'))
        self.sublink_url = TextInput(text='', font_size='16sp', background_color=(0.3, 0.3, 0.3, 1), foreground_color=(1, 1, 1, 1))
        sublink_layout.add_widget(self.sublink_url)

        sublink_buttons_layout = BoxLayout(size_hint=(1, None), size=(900, 60), spacing=10)
        deploy_bot_button = Button(text='Deploy Bot', size_hint_y=1, height=60, background_color =(0.2, 0.6, 0.8, 1))
        deploy_bot_button.bind(on_press=self.deploy_bot)
        sublink_buttons_layout.add_widget(deploy_bot_button)
        sublink_buttons_layout.add_widget(Button(text='Clear', on_press=self.clear_linkscraper, size_hint_y=None, height=60, background_color =(0.2, 0.6, 0.8, 1)))
        sublink_layout.add_widget(sublink_buttons_layout)

        root_layout.add_widget(sublink_layout)

        return root_layout


    def clear_prog(self, instance):
        pass

    def clear_linkscraper(self, instance):
        self.sublink_url.text = ''

    def clear_csv_input(self, instance):
        self.csv_filename_entry.text = ''

    def deploy_bot(self, instance):
        query = self.sublink_url.text.strip()
        if query:
            # Run the custom_google_search function in a separate thread to avoid blocking the UI
            Thread(target=self.run_custom_google_search, args=(query,)).start()
        else:
            popup = CustomPopup("Error", "Please enter a search query.")
            popup.open()

    def run_custom_google_search(self, query):
        custom_google_search(query)


    def delete_file(self, instance):
        file_path = 'results.csv'

        # Function to delete the specified file
        if os.path.exists(file_path):
            os.remove(file_path)
            popup = CustomPopup("File Deleted", f"File '{os.path.basename(file_path)}' deleted successfully.")
            popup.open()
        else:
            popup = CustomPopup("File Not Found", f"File '{os.path.basename(file_path)}' not found.")
            popup.open()

    def quit_app(self, instance):
        # Create and display the custom popup
        intro_message = ("All data in process will be aborted.\n\n\n\n"
                         "Click off the popup to cancel.\n\n\n\n")
        popup = CustomPopup("Are you sure you want to quit?", intro_message)
        popup.open()

        # Bind a function to execute when the popup is dismissed
        popup.bind(on_dismiss=self.check_quit)

    def guide_message(self, instance):
        # Create and display the custom popup
        popup = CustomPopup("Guide:", "This application helps you generate leads in your area\n\n"
                                       "To use the application:\n"
                                       "- Enter a search for a type of business and a location that you want to search in.\n"
                                       "- Click on the 'Search' button to locate the leads in the area.\n"
                                       "- It will ask if you want to save the data to a spreadsheet in CSV format\n"
                                       "- The delete file option will allow you to delete older files that you have created in this folder.\n\n"
                                       "Enjoy finding leads with Lead Generator!\n\n\n\n")
        popup.open()

    def Features_Message(self, instance):
        # Create and display another custom popup
        popup = CustomPopup("Features available", "Various Functions:\n\n"
                                                  "- Clear Last Search: Clears the last recent search and deletes the .csv file. \n"
                                                  "- Preview Data: Choose from the data files that you have created to see what you have available or veiw the \n   raw data in .csv further analysis \n"
                                                  "- Exit to quit.\n\n"
                                                   "Enjoy finding leads with Lead Generator!\n\n\n\n")
        popup.open()

    def searchfunc_popup(self, instance):
        # Create an instance of AnalyzePopup
        search_popup = SearchPopup()

        # Open the AnalyzePopup
        search_popup.open()
        search_popup.bind(on_dismiss=lambda instance, data: print(f"Filename: {data[0]}, File Type: {data[1]}"))

    def preview_data(self, instance):
        file_path = 'results.csv'
        
        if os.path.exists(file_path):
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(('open', file_path))
            else:  # Linux and others
                subprocess.call(('xdg-open', file_path))
        else:
            popup = CustomPopup("Error", f"File '{file_path}' not found.")
            popup.open()


    def check_quit(self, instance):
        # Check if the user confirmed quitting
        if instance.is_confirmed:
            # Quit the app
            App.get_running_app().stop()


if __name__ == '__main__':
    LeadGenerator().run()






















