const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  sendEvent: (eventData) => ipcRenderer.send('event-detected', eventData),
});
