// Handle popup vs sidebar logic
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'OPEN_SIDEBAR') {
    // Get the current window to open sidebar
    chrome.windows.getCurrent((window) => {
      if (window) {
        chrome.sidePanel.open({ windowId: window.id })
          .then(() => {
            console.log('Sidebar opened successfully');
            sendResponse({ success: true });
          })
          .catch((error) => {
            console.error('Error opening sidebar:', error);
            // Try alternative method if first fails
            if (message.tabId) {
              chrome.tabs.get(message.tabId, (tab) => {
                if (tab) {
                  chrome.sidePanel.open({ windowId: tab.windowId })
                    .then(() => {
                      sendResponse({ success: true });
                    })
                    .catch((err) => {
                      console.error('Error opening sidebar (fallback):', err);
                      sendResponse({ success: false, error: err.message });
                    });
                } else {
                  sendResponse({ success: false, error: 'Could not get tab or window' });
                }
              });
            } else {
              sendResponse({ success: false, error: error.message });
            }
          });
      } else {
        sendResponse({ success: false, error: 'Could not get current window' });
      }
    });
    return true; // Keep message channel open for async response
  } else if (message.type === 'START_JOB_APPLICATION') {
    // Handle job application start - call backend scraper
    console.log('Starting job application for:', message.tabUrl);
    console.log('User ID received:', message.userId);
    
    // First, check if backend server is running with a health check
    const healthCheckPromise = fetch('http://127.0.0.1:5001/api/health', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    }).catch(() => null); // Ignore errors for health check
    
    // Prepare request body
    const requestBody = {
      job_url: message.tabUrl
    };
    
    // Add user_id if provided (to fetch resume from Supabase database)
    if (message.userId) {
      requestBody.user_id = message.userId;
      console.log('Adding user_id to request body:', message.userId);
      console.log('Backend will fetch resume from Supabase using this user_id');
    } else {
      console.warn('No user_id provided - backend will require resume data');
    }
    
    console.log('Request body being sent to backend:', JSON.stringify(requestBody, null, 2));
    
    // Check health first, then proceed with the main request
    healthCheckPromise.then(healthResponse => {
      if (!healthResponse || !healthResponse.ok) {
        throw new Error('Backend server is not running. Please start it with:\n\ncd backend && python api_server.py\n\nThe server should be running on port 5001.');
      }
      
      // Call backend API to scrape and tailor resume
      // Using port 5001 to avoid macOS AirPlay interference on port 5000
      return fetch('http://127.0.0.1:5001/api/scrape-and-tailor', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });
    })
    .then(response => {
      if (!response) {
        throw new Error('Backend server is not running. Please start it with:\n\ncd backend && python api_server.py');
      }
      // Check if response is ok
      if (!response.ok) {
        return response.text().then(text => {
          throw new Error(`Server error (${response.status}): ${text || response.statusText}`);
        });
      }
      // Check if response has content
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        return response.text().then(text => {
          throw new Error(`Invalid response type. Expected JSON, got: ${contentType}. Response: ${text.substring(0, 200)}`);
        });
      }
      return response.json();
    })
    .then(data => {
      console.log('Backend response received:', data);
      sendResponse({ 
        success: data.success, 
        job_data: data.job_data,
        ai_response: data.ai_response,
        formatted_prompt: data.formatted_prompt,
        improvements: data.improvements,
        rewritten_resume: data.rewritten_resume,
        pdf_path: data.pdf_path,
        error: data.error 
      });
    })
    .catch(error => {
      console.error('Error calling backend API:', error);
      let errorMessage = error.message;
      
      // Provide helpful error messages
      if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        errorMessage = 'Cannot connect to backend server. Make sure the API server is running:\n\ncd backend && python api_server.py\n\nThe server should be running on port 5001.';
      } else if (error.message.includes('Unexpected end of JSON input')) {
        errorMessage = 'Backend server returned invalid response. Check if the server is running and responding correctly.';
      }
      
      sendResponse({ 
        success: false, 
        error: `Failed to connect to backend: ${errorMessage}` 
      });
    });
    
    return true; // Keep message channel open for async response
  } else if (message.type === 'DOWNLOAD_RESUME') {
    // Handle resume download
    const pdfPath = message.pdf_path;
    
    if (!pdfPath) {
      sendResponse({ 
        success: false, 
        error: 'No PDF path provided' 
      });
      return true;
    }
    
    console.log('Downloading tailored resume from:', pdfPath);
    
    // Construct download URL
    const downloadUrl = `http://127.0.0.1:5001/api/download-resume?pdf_path=${encodeURIComponent(pdfPath)}`;
    
    // Use Chrome downloads API to download the file
    chrome.downloads.download({
      url: downloadUrl,
      saveAs: true, // Show save dialog
      conflictAction: 'uniquify' // If file exists, create unique name
    }, (downloadId) => {
      if (chrome.runtime.lastError) {
        console.error('Download error:', chrome.runtime.lastError);
        sendResponse({ 
          success: false, 
          error: chrome.runtime.lastError.message 
        });
      } else {
        console.log('Download started with ID:', downloadId);
        sendResponse({ success: true });
      }
    });
    
    return true; // Keep message channel open for async response
  } else if (message.type === 'VIEW_RESUME') {
    // Handle resume preview
    // TODO: Integrate with backend
    console.log('Opening resume preview...');
    sendResponse({ success: true });
  } else if (message.type === "START_AUTOMATION") {
    chrome.tabs.create({ url: message.productUrl }, (tab) => {
      // Wait until the new tab is fully loaded
      const listener = (tabId, info) => {
        if (tabId === tab.id && info.status === "complete") {
          // First inject the content script
          console.log(info.status);
          chrome.scripting.executeScript({
            target: { tabId },
            files: ["content.js"],
          });
          // Remove the listener so it doesn't run multiple times
          chrome.tabs.onUpdated.removeListener(listener);
        }
      };

      chrome.tabs.onUpdated.addListener(listener);
    });
    sendResponse({ success: true });
  }
  return true; // Keep message channel open for async response
});

// Set sidebar behavior - but don't open on action click since we have popup
chrome.sidePanel
  .setPanelBehavior({ openPanelOnActionClick: false })
  .catch((error) => console.error(error));

chrome.runtime.onInstalled.addListener((details) => {
  // Extension installed - no automatic tab opening
  console.log("Clueless-to-Careers-Agent installed");
});

let actionMenu = false;
if (chrome.contextMenus && !actionMenu) {
  actionMenu = true;

  chrome.contextMenus.create({
    id: "welcome-guide",
    title: "Welcome Guide",
    contexts: ["all"],
  });

  chrome.contextMenus.create({
    id: "connect-with-me-on-linkedin",
    title: "Connect With Me On Linkedin",
    contexts: ["all"],
  });

  // Add "Share this" parent menu
  const shareParent = chrome.contextMenus.create({
    id: "share-this",
    title: "Share this",
    contexts: ["all"],
  });

  // Add social media share options
  const shareOptions = [
    {
      id: "share-email",
      title: "Email",
      url: "mailto:?subject=Check out FlashSlide&body=",
    },
    {
      id: "share-x",
      title: "X (Twitter)",
      url: "https://twitter.com/intent/tweet?text=",
    },
    {
      id: "share-facebook",
      title: "Facebook",
      url: "https://www.facebook.com/sharer/sharer.php?u=",
    },
    {
      id: "share-whatsapp",
      title: "WhatsApp",
      url: "https://api.whatsapp.com/send?text=",
    },
    {
      id: "share-linkedin",
      title: "LinkedIn",
      url: "https://www.linkedin.com/shareArticle?mini=true&url=",
    },
    {
      id: "share-telegram",
      title: "Telegram",
      url: "https://t.me/share/url?url=",
    },
    {
      id: "share-vkontakte",
      title: "VKontakte",
      url: "https://vk.com/share.php?url=",
    },
  ];

  shareOptions.forEach((option) => {
    chrome.contextMenus.create({
      id: option.id,
      title: option.title,
      parentId: shareParent,
      contexts: ["all"],
    });
  });

  // Add a click handler for the context menu items
  chrome.contextMenus.onClicked.addListener((info, tab) => {
    const extensionPage = "";
    const shareMessage = encodeURIComponent(
      "Check out FlashSlide Chrome Extension: " + extensionPage
    );

    switch (info.menuItemId) {
      case "welcome-guide":
        chrome.tabs.create({
          url: "https://github.com/NikkiAung/Flash-Slide/blob/main/README.md",
          active: true,
        });
        break;
      case "connect-with-me-on-linkedin":
        chrome.tabs.create({
          url: "https://www.linkedin.com/in/aung-nanda-oo-8962292b2/",
          active: true,
        });
        break;
      case "share-email":
        chrome.tabs.create({ url: `${shareOptions[0].url}${shareMessage}` });
        break;
      case "share-x":
        chrome.tabs.create({ url: `${shareOptions[1].url}${shareMessage}` });
        break;
      case "share-facebook":
        chrome.tabs.create({ url: `${shareOptions[2].url}${extensionPage}` });
        break;
      case "share-whatsapp":
        chrome.tabs.create({ url: `${shareOptions[3].url}${shareMessage}` });
        break;
      case "share-linkedin":
        chrome.tabs.create({
          url: `${
            shareOptions[4].url
          }${extensionPage}&title=${encodeURIComponent(
            "FlashSlide Chrome Extension"
          )}`,
        });
        break;
      case "share-telegram":
        chrome.tabs.create({
          url: `${shareOptions[5].url}${extensionPage}&text=${shareMessage}`,
        });
        break;
      case "share-vkontakte":
        chrome.tabs.create({ url: `${shareOptions[6].url}${extensionPage}` });
        break;
    }
  });
}

