import os
import requests
import webbrowser
import sys
import random
import string
from datetime import datetime, timedelta
from colorama import Fore, Style, init
import time
import threading
from bs4 import BeautifulSoup  # Importing BeautifulSoup for web scraping

# Initialize colorama
init(autoreset=True)

API_KEY = "3dd5f0a86481cb6424c236a0693b719f"  # Your OpenWeatherMap API key
NOTES_FILE = "notes.txt"

def banner():
    print(Fore.MAGENTA + Style.BRIGHT + """
    ███████╗██╗  ██╗██╗   ██╗██╗███████╗██╗  ██╗██╗  ██╗
    ██╔════╝██║  ██║██║   ██║██║██╔════╝██║  ██║██║  ██║
    █████╗  ███████║██║   ██║██║█████╗  ███████║███████║
    ██╔══╝  ██╔══██║██║   ██║██║██╔══╝  ██╔══██║██╔══██║
    ███████╗██║  ██║╚██████╔╝██║███████╗██║  ██║██║  ██║
    ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
    """)
    print(Fore.CYAN + Style.BRIGHT + "Welcome to the Ultimate Python Toolkit!\n")

def hide_file():
    filename = input(Fore.YELLOW + "Enter the name of the file to hide: ")
    if os.path.exists(filename):
        new_name = '.' + filename  # Prefixing with dot to hide
        os.rename(filename, new_name)
        print(Fore.GREEN + f"File '{filename}' hidden as '{new_name}'.")
    else:
        print(Fore.RED + "File does not exist.")

def list_directory():
    print(Fore.CYAN + "\nCurrent Directory Files:")
    for item in os.listdir('.'):
        print(Fore.YELLOW + f"- {item}")

def simple_calculator():
    print(Fore.CYAN + "\nSimple Calculator")
    try:
        num1 = float(input(Fore.YELLOW + "Enter first number: "))
        operator = input(Fore.YELLOW + "Enter operator (+, -, *, /): ")
        num2 = float(input(Fore.YELLOW + "Enter second number: "))
        
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            result = num1 / num2
        else:
            print(Fore.RED + "Invalid operator!")
            return
        
        print(Fore.GREEN + f"Result: {result}")
    except ValueError:
        print(Fore.RED + "Invalid input! Please enter numbers only.")

def get_weather():
    city = input(Fore.YELLOW + "Enter the city name: ")
    url = f"https://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&appid={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        weather_description = data['weather'][0]['description']
        print(Fore.GREEN + f"Current temperature in {city}: {temp}°C")
        print(Fore.GREEN + f"Weather description: {weather_description.capitalize()}")
    else:
        print(Fore.RED + "City not found. Please check the name and try again.")

def open_browser():
    url = input(Fore.YELLOW + "Enter the URL to open: ")
    webbrowser.open(url)
    print(Fore.GREEN + f"Opening {url} in your default web browser.")

def shutdown_system():
    confirm = input(Fore.YELLOW + "Are you sure you want to shut down the system? (yes/no): ")
    if confirm.lower() == 'yes':
        print(Fore.RED + "Shutting down the system...")
        os.system("shutdown /s /t 1")  # Windows shutdown command
    else:
        print(Fore.GREEN + "Shutdown canceled.")

def birthday_calculator():
    birth_date = input(Fore.YELLOW + "Enter your birth date (YYYY-MM-DD): ")
    try:
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        next_birthday = datetime(today.year, birth_date.month, birth_date.day)
        
        if today > next_birthday:
            next_birthday = datetime(today.year + 1, birth_date.month, birth_date.day)

        days_until_birthday = (next_birthday - today).days
        
        print(Fore.GREEN + f"You are {age} years old.")
        print(Fore.GREEN + f"Your next birthday is in {days_until_birthday} days.")
    except ValueError:
        print(Fore.RED + "Invalid date format! Please use YYYY-MM-DD.")

def christmas_countdown():
    today = datetime.now()
    christmas = datetime(today.year, 12, 25)
    
    if today > christmas:
        christmas = datetime(today.year + 1, 12, 25)

    days_until_christmas = (christmas - today).days
    print(Fore.GREEN + f"There are {days_until_christmas} days left until Christmas!")

def set_reminder():
    reminder_date = input(Fore.YELLOW + "Enter the reminder date (YYYY-MM-DD): ")
    reminder_time = input(Fore.YELLOW + "Enter the reminder time (HH:MM 24-hour format): ")
    reminder_message = input(Fore.YELLOW + "Enter the reminder message: ")
    
    try:
        reminder_datetime = datetime.strptime(f"{reminder_date} {reminder_time}", '%Y-%m-%d %H:%M')
        print(Fore.GREEN + f"Reminder set for {reminder_datetime}.")
        
        # Start a thread for the reminder countdown
        threading.Thread(target=reminder_thread, args=(reminder_datetime, reminder_message)).start()
    except ValueError:
        print(Fore.RED + "Invalid date or time format!")

def reminder_thread(reminder_datetime, message):
    while True:
        now = datetime.now()
        if now >= reminder_datetime:
            print(Fore.YELLOW + f"\nReminder: {message}")
            break
        time.sleep(30)  # Check every 30 seconds

def organize_files():
    print(Fore.CYAN + "\nOrganizing files...")
    file_types = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif'],
        'Documents': ['.pdf', '.docx', '.txt', '.xlsx'],
        'Videos': ['.mp4', '.mov', '.avi'],
        'Music': ['.mp3', '.wav'],
        'Archives': ['.zip', '.tar', '.gz'],
    }

    for folder, extensions in file_types.items():
        if not os.path.exists(folder):
            os.makedirs(folder)

    for file in os.listdir('.'):
        for folder, extensions in file_types.items():
            if any(file.endswith(ext) for ext in extensions):
                os.rename(file, os.path.join(folder, file))
                print(Fore.GREEN + f"Moved '{file}' to '{folder}/'")

def todo_list():
    tasks = []
    while True:
        print(Fore.CYAN + "\nTo-Do List:")
        for index, task in enumerate(tasks, start=1):
            print(Fore.YELLOW + f"{index}. {task}")
        print(Fore.YELLOW + "Enter a task or type 'exit' to finish:")
        
        task = input()
        if task.lower() == 'exit':
            break
        tasks.append(task)

def random_password_generator():
    length = int(input(Fore.YELLOW + "Enter the desired password length: "))
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    print(Fore.GREEN + f"Generated Password: {password}")

def number_guessing_game():
    number = random.randint(1, 100)
    attempts = 0
    print(Fore.CYAN + "\nGuess the number (between 1 and 100):")
    
    while True:
        guess = int(input(Fore.YELLOW + "Your guess: "))
        attempts += 1
        
        if guess < number:
            print(Fore.RED + "Too low! Try again.")
        elif guess > number:
            print(Fore.RED + "Too high! Try again.")
        else:
            print(Fore.GREEN + f"Congratulations! You've guessed the number {number} in {attempts} attempts.")
            break

def notes():
    print(Fore.CYAN + "\nNotes")
    if not os.path.exists(NOTES_FILE):
        open(NOTES_FILE, 'w').close()

    while True:
        print(Fore.YELLOW + "\n1. Add a Note")
        print(Fore.YELLOW + "2. View Notes")
        print(Fore.YELLOW + "3. Delete a Note")
        print(Fore.YELLOW + "4. Exit Notes")
        
        choice = input(Fore.YELLOW + "Select an option: ")
        
        if choice == '1':
            note = input(Fore.YELLOW + "Enter your note: ")
            with open(NOTES_FILE, 'a') as f:
                f.write(note + "\n")
            print(Fore.GREEN + "Note added!")
        
        elif choice == '2':
            print(Fore.CYAN + "\nYour Notes:")
            with open(NOTES_FILE, 'r') as f:
                notes = f.readlines()
                for i, note in enumerate(notes, start=1):
                    print(Fore.YELLOW + f"{i}. {note.strip()}")
        
        elif choice == '3':
            print(Fore.CYAN + "\nYour Notes:")
            with open(NOTES_FILE, 'r') as f:
                notes = f.readlines()
                for i, note in enumerate(notes, start=1):
                    print(Fore.YELLOW + f"{i}. {note.strip()}")
            note_number = int(input(Fore.YELLOW + "Enter the note number to delete: "))
            notes.pop(note_number - 1)
            with open(NOTES_FILE, 'w') as f:
                f.writelines(notes)
            print(Fore.GREEN + "Note deleted!")
        
        elif choice == '4':
            break

def web_scraper():
    url = input(Fore.YELLOW + "Enter the URL to scrape: ")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example: Scrape all paragraph text
        paragraphs = soup.find_all('p')
        print(Fore.CYAN + "\nScraped Paragraphs:")
        for p in paragraphs:
            print(Fore.YELLOW + p.get_text())
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"An error occurred: {e}")

def random_quote_generator():
    try:
        response = requests.get("https://api.quotable.io/random")
        response.raise_for_status()
        quote_data = response.json()
        quote = quote_data['content']
        author = quote_data['author']
        print(Fore.GREEN + f"\nQuote: \"{quote}\" - {author}")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"An error occurred: {e}")

def main():
    banner()
    
    while True:
        print(Fore.CYAN + "\nAvailable tools:")
        print(Fore.GREEN + "1. Hide a file")
        print(Fore.GREEN + "2. List current directory files")
        print(Fore.GREEN + "3. Simple Calculator")
        print(Fore.GREEN + "4. Get Current Weather")
        print(Fore.GREEN + "5. Open Web Browser")
        print(Fore.GREEN + "6. Shut Down the System")
        print(Fore.GREEN + "7. Birthday Calculator")
        print(Fore.GREEN + "8. Christmas Countdown")
        print(Fore.GREEN + "9. Set a Reminder")
        print(Fore.GREEN + "10. Organize Files")
        print(Fore.GREEN + "11. To-Do List")
        print(Fore.GREEN + "12. Random Password Generator")
        print(Fore.GREEN + "13. Number Guessing Game")
        print(Fore.GREEN + "14. Notes")
        print(Fore.GREEN + "15. Web Scraper")
        print(Fore.GREEN + "16. Random Quote Generator")  # Added random quote generator option
        print(Fore.GREEN + "17. Exit")
        
        choice = input(Fore.YELLOW + "Select a tool (1-17): ")
        
        if choice == '1':
            hide_file()
        elif choice == '2':
            list_directory()
        elif choice == '3':
            simple_calculator()
        elif choice == '4':
            get_weather()
        elif choice == '5':
            open_browser()
        elif choice == '6':
            shutdown_system()
        elif choice == '7':
            birthday_calculator()
        elif choice == '8':
            christmas_countdown()
        elif choice == '9':
            set_reminder()
        elif choice == '10':
            organize_files()
        elif choice == '11':
            todo_list()
        elif choice == '12':
            random_password_generator()
        elif choice == '13':
            number_guessing_game()
        elif choice == '14':
            notes()
        elif choice == '15':
            web_scraper()
        elif choice == '16':
            random_quote_generator()  # Call the random quote generator function
        elif choice == '17':
            print(Fore.RED + "Exiting the toolkit. Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice. Please select again.")
    
    input(Fore.YELLOW + "Press Enter to exit...")

if __name__ == "__main__":
    main()
