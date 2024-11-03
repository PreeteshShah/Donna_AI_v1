import pytesseract
from PIL import Image
import pyautogui
import openai
import time
import requests
import mysql.connector

# OpenAI API Key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Tesseract OCR setup
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# MySQL connection details
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'event_manager'
}

def insert_event(event_name, event_date, event_time, place, category_type, priority='Medium'):
    """Insert detected event into the MySQL database."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
        INSERT INTO events (event_name, event_date, event_time, place, category_type, priority)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (event_name, event_date, event_time, place, category_type, priority)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        print("Event inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def capture_screen():
    screenshot = pyautogui.screenshot()
    return screenshot

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

def analyze_text(input_text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Extract event details from this text: {input_text}",
        max_tokens=100
    )
    return response['choices'][0]['text'].strip()

def process_event_details(event_details):
    # For demonstration, let's assume `event_details` is parsed into relevant fields.
    # In real application, parse `event_details` properly.
    event_name = "Sample Event"
    event_date = "2024-11-15"
    event_time = "10:00:00"
    place = "Office"
    category_type = "Meeting"
    priority = "High"
    
    insert_event(event_name, event_date, event_time, place, category_type, priority)

def main():
    while True:
        image = capture_screen()
        text = extract_text_from_image(image)
        if text.strip():
            event_info = analyze_text(text)
            if event_info:
                process_event_details(event_info)
        time.sleep(10)

if __name__ == "__main__":
    main()
