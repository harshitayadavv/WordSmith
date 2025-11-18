chrome.runtime.onInstalled.addListener(() => {
  console.log('WordSmith extension installed');
});

// Handle extension click
chrome.action.onClicked.addListener((tab) => {
  // This is handled by the popup, but we can add additional functionality here if needed
  console.log('WordSmith extension clicked');
});
