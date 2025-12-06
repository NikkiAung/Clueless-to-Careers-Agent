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
    // Handle job application start
    // TODO: Integrate with backend AI agent
    console.log('Starting job application for:', message.tabUrl);
    sendResponse({ success: true });
  } else if (message.type === 'DOWNLOAD_RESUME') {
    // Handle resume download
    // TODO: Integrate with backend
    console.log('Downloading tailored resume...');
    sendResponse({ success: true });
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

