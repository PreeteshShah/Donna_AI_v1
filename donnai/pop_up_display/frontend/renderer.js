function checkForEvent() {
    const textInput = document.getElementById('text-input').value;
  
    // Dummy event detection (you can replace this with actual detection logic)
    const eventRegex = /(\b\d{1,2}\/\d{1,2}\/\d{2,4}\b|\b\d{1,2}:\d{2}\b)/;
    const eventMatch = textInput.match(eventRegex);
  
    if (eventMatch) {
      const eventData = `Detected date/time: ${eventMatch[0]}`;
      window.electronAPI.sendEvent(eventData);
    } else {
      alert('No event detected.');
    }
  }
  