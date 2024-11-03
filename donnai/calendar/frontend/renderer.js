const axios = require('axios');

document.addEventListener('DOMContentLoaded', () => {
  axios.get('http://127.0.0.1:8000/api/events/')
    .then(response => {
      const events = response.data;
      const eventsDiv = document.getElementById('events');
      events.forEach(event => {
        const eventElement = document.createElement('div');
        eventElement.innerHTML = `<p>${event.event_name} - ${event.event_date} ${event.event_time} at ${event.place}</p>`;
        eventsDiv.appendChild(eventElement);
      });
    })
    .catch(error => {
      console.error('Error fetching events:', error);
    });
});
