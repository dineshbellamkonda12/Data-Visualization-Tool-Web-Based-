## Project Name
Visualization App

## Description
Visualization App is a web application that allows users to to be able to interact, extract and filter data from the chart based on their condition. It is built using Python Django for the backend and HTML, CSS and Javascript for the frontend.

## Installation
Follow the instructions below to get the project up and running on your local machine.
These instructions will guide you through setting up and running the Django web application on your local computer.

Prerequisites:
Python (version 3.11.3 or higher)
pip (Python package manager)
Git

1. Clone the Repository
Clone the project repository from the source control repository using Git: git clone https://github.com/dineshbellamkonda12/Data-Visualization-Tool-Web-Based-.git

2. Create and Activate Virtual Environment (Optional but Recommended)
Navigate to the project directory and create a virtual environment using below commands:

cd your_project_directory
python -m venv venv

Activate the virtual environment:
On Windows:
venv\Scripts\activate

On macOS and Linux:
source venv/bin/activate

3. Install Dependencies
Install the required Python packages listed in the requirements.txt file:
pip install -r requirements.txt

4. Import Data 
Run importdata.py script that inserts CSV data into the inbuilt Django SQLite database:
python importdata.py

5. Run Migrations
Apply the database migrations to create the required tables:
python manage.py migrate

6. Run the Development Server
Start the Django development server to run the application:
python manage.py runserver

## Repository Information
stanpro -> Django Project
stanapp -> Django App 