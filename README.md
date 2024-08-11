
# Lead Generator Application

## Overview
The Lead Generator application is designed to help users generate leads in their area using Google Maps search. It provides a user-friendly interface with various features to manage and preview the generated data.

## Features
- **Clear Last Search**: Clears the last recent search and deletes the `results.csv` file.
- **Preview Data**: Allows users to preview the data files they have created, viewing raw data in `.csv`, `.xml`, or `.xlsx` format for further analysis.
- **Exit**: Exits the application.
- **Google Map Search**: Enter a search query to locate leads in a specific area.

## Installation
1. Ensure you have Python installed on your system.
2. Install the required dependencies:
   ```bash
   pip install kivy

3. May need to install other libraries depending on what you have installed.

## Usage
Run the application:
python GUI.py

Use the interface to enter your search query and generate leads.
Code Structure

## LeadGenerator Class: 
Main application class that builds the UI and handles user interactions.

## Google Maps Bot Class:

- Uses Selnium framework for automating a google maps search.
- Scrapes informatiom about location, reviews, rating, and website.
- Saves to a .csv file.

## GUI Popups Class:

- Handles all the popup functions used in the GUI class.