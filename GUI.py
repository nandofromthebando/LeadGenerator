import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget  # Import Widget for separators
from kivy.core.window import Window
from kivy.uix.popup import Popup
import tkinter as tk
from tkinter import messagebox
from textblob import TextBlob
from newspaper import Article
import subprocess
from GUI_Features import CustomPopup , AnalyzePopup , Sites_to_Scrape

class LeadGenerator(App):

    def build(self):

        # Set window size to match screen dimensions
        Window.fullscreen = 'auto'
        # Setting background color
        Window.clearcolor = (0.133, 0.133, 0.133, 1)

        root_layout = BoxLayout(orientation='vertical', size_hint=(1, 1), padding=20, spacing=10)
        root_layout.bind(minimum_height=root_layout.setter('height'))

        # Align widgets vertically centered
        for child in root_layout.children:
            child.size_hint_y = None
            child.height = '60dp'  # Set fixed height
            child.pos_hint = {'center_x': 0.5}  # Center horizontally

        # Center the layout on the screen
        root_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Menu bar
        menu_layout = BoxLayout(size_hint=(1, None), padding=10, spacing=10)

        # Menu buttons
        menu_statistics_button = Button(text='Statistics', size_hint=(None, None), size=(250, 60))
        menu_statistics_button.text_size = menu_statistics_button.size
        menu_statistics_button.halign = 'center'
        menu_statistics_button.valign = 'middle'

        menu_preview_data_button = Button(text='Preview Data', size_hint=(None, None), size=(250, 60))
        menu_preview_data_button.text_size = menu_preview_data_button.size
        menu_preview_data_button.halign = 'center'
        menu_preview_data_button.valign = 'middle'

        menu_find_sites_button = Button(text='Find Sites to Scrape', size_hint=(None, None), size=(400, 60))
        menu_find_sites_button.bind(on_press=self.Find_Sites_to_Scrape)
        menu_find_sites_button.text_size = menu_find_sites_button.size
        menu_find_sites_button.halign = 'center'
        menu_find_sites_button.valign = 'middle'

        menu_exit_button = Button(text='Exit', size_hint=(None, None), size=(100, 60), on_press=self.quit_app)
        menu_exit_button.text_size = menu_exit_button.size
        menu_exit_button.halign = 'center'
        menu_exit_button.valign = 'middle'

        status_bar = Label(text='Ready', size_hint=(1, None), height=60, color=(1, 1, 1, 1))

        menu_layout.add_widget(menu_statistics_button)
        menu_layout.add_widget(menu_preview_data_button)
        menu_layout.add_widget(menu_find_sites_button)
        menu_layout.add_widget(menu_exit_button)
        menu_layout.add_widget(status_bar)
        root_layout.add_widget(menu_layout)

        # Horizontal separator
        root_layout.add_widget(Widget(size_hint_y=None, height=5))

        # Guide message
        welcome_message = "Welcome to DeepScrape!"
        welcome_label = Label(text=welcome_message, font_size='24sp', bold=True, color=(1, 1, 1, 1), size_hint=(1, None), height=60, halign='center')
        root_layout.add_widget(welcome_label)

        # Add buttons to create custom popups
        button1 = Button(text='Start Here', size_hint=(None, None), size=(150, 60))
        button1.bind(on_press=self.guide_message)
        button2 = Button(text='Features', size_hint=(None, None), size=(150, 60))
        button2.bind(on_press=self.Features_Message)

        buttons_layout = BoxLayout(size_hint=(None, None), size=(300, 120), spacing=10)
        buttons_layout.add_widget(button1)
        buttons_layout.add_widget(button2)
        root_layout.add_widget(buttons_layout)

        # Horizontal separator
        root_layout.add_widget(Widget(size_hint_y=None, height=2))

        url_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.7), spacing=10, padding=(0, 10))
        url_layout.add_widget(Label(text="Scrape Links:", font_size='24sp', bold=True, color=(1, 1, 1, 1)))
        self.url_text = TextInput(text='', font_size='12sp', background_color=(0.3, 0.3, 0.3, 1))
        url_layout.add_widget(self.url_text)
        url_buttons_layout = BoxLayout(size_hint=(1, None), height=60, spacing=10)
        url_buttons_layout.add_widget(Button(text='Clear', on_press=self.clear_url_text))

        url_buttons_layout.add_widget(Button(text='Analyze', on_press=self.analyze_popup))
        url_layout.add_widget(url_buttons_layout)
        root_layout.add_widget(url_layout)

        sublink_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=60)
        sublink_layout.add_widget(Label(text="Scrape For Sublinks:", font_size='18sp', bold=True, color=(1, 1, 1, 1)))
        self.sublink_url = TextInput(text='', font_size='16sp', background_color=(0.3, 0.3, 0.3, 1))
        sublink_layout.add_widget(self.sublink_url)

        sublink_buttons_layout = BoxLayout(size_hint=(1, None), size=(900, 60), spacing=10)
        sublink_buttons_layout.add_widget(Button(text='Scrape Sublinks', size_hint_y=1, height=60))
        sublink_buttons_layout.add_widget(Button(text='Clear', on_press=self.clear_linkscraper, size_hint_y=None, height=60))
        sublink_layout.add_widget(sublink_buttons_layout)

        filename_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=60)
        filename_layout.add_widget(Label(text="Filename To delete:", font_size='18sp', bold=True, color=(1, 1, 1, 1)))
        self.csv_filename_entry = TextInput(text='', font_size='16sp', background_color=(0.3, 0.3, 0.3, 1))
        filename_layout.add_widget(self.csv_filename_entry)

        filename_buttons_layout = BoxLayout(size_hint=(1, None), size=(900, 60), spacing=10)
        filename_buttons_layout.add_widget(Button(text='Delete File', on_press=self.delete_file, size_hint_y=None, height=60))
        filename_buttons_layout.add_widget(Button(text='Clear', on_press=self.clear_csv_input, size_hint_y=None, height=60))
        filename_layout.add_widget(filename_buttons_layout)

        root_layout.add_widget(sublink_layout)
        root_layout.add_widget(filename_layout)

        return root_layout

    def summarize(self, instance):
            filename = self.analyze_file_entry.text
            selected_format = self.selected_format.get()

            # Grabs URLs from user and analyzes them
            urls = self.filename_entry.text.strip().split('\n')

            def save_data(file_format, filename):
                for url in urls:
                    if url.strip():
                        try:
                            article = Article(url)
                            article.download()
                            article.parse()
                            article.nlp()

                            # Extracting data from the article
                            article_title = article.title
                            article_authors = ', '.join(article.authors)
                            article_publish_date = str(article.publish_date)
                            article_summary = article.summary
                            article_text = article.text
                            analysis = TextBlob(article_text)
                            article_sentiment = str(analysis.polarity)

                            # Save data to the selected file format with the provided filename
                            if file_format == 'CSV':
                                save_titles_to_csv([url], [article_title], [article_authors], [article_publish_date],
                                                [article_summary], [article_sentiment], f"{filename}.csv")
                            elif file_format == 'XLS':
                                save_titles_to_xls([url], [article_title], [article_authors], [article_publish_date],
                                                [article_summary], [article_sentiment], f"{filename}.xls")
                            elif file_format == 'XML':
                                save_titles_to_xml([url], [article_title], [article_authors], [article_publish_date],
                                                [article_summary], [article_sentiment], f"{filename}.xml")

                        except Exception as e:
                            print(f"Error processing URL: {url}. Error: {e}")
                            continue

                    file_path = f"{filename}.csv" if file_format == 'CSV' else (
                        f"{filename}.xls" if file_format == 'XLS' else f"{filename}.xml")
                    subprocess.Popen(["open", file_path])  # Opens the saved file

            # Call the save_data function with selected_format and filename
            save_data(selected_format, filename)

    def scrape_and_display(self):
        url = self.sublink_url.text
        sublinks = scrape_the_goods(url)
        if sublinks:
            self.url_text.text = '\n'.join(sublinks)
        else:
            self.url_text.text = "No sublinks found."

    def clear_url_text(self, instance):
        self.url_text.text = ''

    def clear_linkscraper(self, instance):
        self.sublink_url.text = ''

    def clear_csv_input(self, instance):
        self.csv_filename_entry.text = ''

    def delete_file(self, instance):

        # Function to delete the specified file
        if os.path.exists((self.csv_filename_entry.text)):
            os.remove((self.csv_filename_entry.text))
            popup = CustomPopup("File Deleted", f"File '{os.path.basename((self.csv_filename_entry.text))}' deleted successfully.")
            popup.open()
        else:
            popup = CustomPopup("File Not Found", f"File '{os.path.basename((self.csv_filename_entry.text))}' not found.")
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
        popup = CustomPopup("Guide:", "This application helps you analyze articles and scrape sublinks from websites.\n\n"
                                       "To use the application:\n"
                                       "- Enter the URL(s) of the news articles you want to analyze in the top section.\n"
                                       "- Click on the 'Analyze' button to summarize the articles.\n"
                                       "- Enter the URL to scrape sublinks from in the bottom section.\n"
                                       "- Click on the 'Scrape Sublinks' button to extract sublinks from the provided URL.\n\n"
                                       "Enjoy analyzing news with Deep Scrape!\n\n\n\n")
        popup.open()

    def Features_Message(self, instance):
        # Create and display another custom popup
        popup = CustomPopup("Features available", "Various Functions:\n\n"
                                                  "- Statistics: Perform statistical analysis of your created data, as well as visualization of availabe data. \n"
                                                  "- Preview Data: Choose from the data files that you have created to see what you have available or veiw the \n   raw data in .csv, , .xml, .xlx format for furhter analysis \n"
                                                  "- Find Sites To Scrape: Various common sites availbe for scraping.\n"
                                                  "- Exit to quit.\n\n"
                                                  "Enjoy analyzing news with Deep Scrape!\n\n\n\n")
        popup.open()

    def analyze_popup(self, instance):
        # Create an instance of AnalyzePopup
        analyze_popup = AnalyzePopup()

        # Open the AnalyzePopup
        analyze_popup.open()
        analyze_popup.bind(on_dismiss=lambda instance, data: print(f"Filename: {data[0]}, File Type: {data[1]}"))

    def Find_Sites_to_Scrape(self, instance):
        # Create an instance of Sites to Scrape
        find_sites = Sites_to_Scrape()

        # Open the AnalyzePopup
        find_sites.open()
    def check_quit(self, instance):
        # Check if the user confirmed quitting
        if instance.is_confirmed:
            # Quit the app
            App.get_running_app().stop()


if __name__ == '__main__':
    NewsAnalyzer().run()






















