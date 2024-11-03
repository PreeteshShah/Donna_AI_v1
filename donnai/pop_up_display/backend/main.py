import pytesseract
from PIL import Image
import pyautogui
import openai
import time
from plyer import notification
import mysql.connector

# Set your OpenAI API key
openai.api_key = 'big secret shhh...'

# Path to Tesseract-OCR executable (modify this according to your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# MySQL connection details
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'event_manager'
}

def capture_screen():
    """Capture the entire screen."""
    screenshot = pyautogui.screenshot()
    return screenshot

def extract_text_from_image(image):
    """Extract text from the given image using Tesseract OCR."""
    text = pytesseract.image_to_string(image)
    return text

def analyze_text(input_text):
    """Use OpenAI API to detect events in the text."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Extract any event-related details (date, time, name, place, category) from the following text:\n{input_text}",
            max_tokens=100
        )
        extracted_info = response['choices'][0]['text'].strip()
        return extracted_info
    except Exception as e:
        return f"Error: {str(e)}"

def display_notification(event_info):
    """Display a desktop notification with event information."""
    notification.notify(
        title='Event Detected',
        message=f"Detected Event: {event_info}\nWould you like to add this to your calendar?",
        app_name='Event Tracker',
        timeout=10  # Notification timeout in seconds
    )

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

def parse_event_details(event_info):
    """Parse event details from the analyzed text."""
    # Simplified parsing logic. This would depend on the format of the response.
    try:
        lines = event_info.split('\n')
        event_details = {
            'event_name': lines[0] if len(lines) > 0 else 'Unknown Event',
            'event_date': lines[1] if len(lines) > 1 else '0000-00-00',
            'event_time': lines[2] if len(lines) > 2 else '00:00:00',
            'place': lines[3] if len(lines) > 3 else 'Unknown Place',
            'category_type': lines[4] if len(lines) > 4 else 'General'
        }
        return event_details
    except Exception as e:
        print(f"Error parsing event details: {e}")
        return None

def main():
    """Main loop to constantly capture screen and analyze text."""
    while True:
        try:
            # Capture the screen
            image = capture_screen()
            # Extract text from the screen
            text = extract_text_from_image(image)
            if text.strip():  # Only process if there's any text
                print("Extracted Text:", text)
                # Analyze the text for events
                event_info = analyze_text(text)
                if event_info and "Error" not in event_info:
                    print("Detected Event Info:", event_info)
                    display_notification(event_info)
                    
                    # Parse event details and insert into DB
                    event_details = parse_event_details(event_info)
                    if event_details:
                        insert_event(
                            event_name=event_details['event_name'],
                            event_date=event_details['event_date'],
                            event_time=event_details['event_time'],
                            place=event_details['place'],
                            category_type=event_details['category_type']
                        )
            else:
                print("No text detected.")
            
            # Wait for a few seconds before capturing again
            time.sleep(10)  # Adjust this interval as needed
        except KeyboardInterrupt:
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
