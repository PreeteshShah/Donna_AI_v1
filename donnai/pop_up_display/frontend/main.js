const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

let mainWindow;

app.on('ready', () => {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      enableRemoteModule: false,
    },
  });

  mainWindow.loadFile('index.html');
});

// Handle event from the renderer process
ipcMain.on('event-detected', (event, eventData) => {
  console.log('Event detected:', eventData);

  const response = {
    title: 'Add Event',
    message: `Event Detected: ${eventData}. Would you like to add it to your calendar?`,
    buttons: ['Yes', 'No'],
  };

  const buttonClicked = require('electron').dialog.showMessageBoxSync(mainWindow, response);
  
  if (buttonClicked === 0) {
    // Call Python script to add event
    const { exec } = require('child_process');
    exec(`python ../main.py "${eventData}"`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error: ${error.message}`);
        return;
      }
      if (stderr) {
        console.error(`stderr: ${stderr}`);
        return;
      }
      console.log(`stdout: ${stdout}`);
    });
  }
});
