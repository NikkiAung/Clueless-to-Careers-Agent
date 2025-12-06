const DEFAULT_URL = "http://localhost:3000";
const SIDEBAR_ITEMS = [
  {
    url: "http://localhost:3000",
    title: "My App",
    icon: "logos/amazon_scraping.png",
  },
];

let currentUrl = DEFAULT_URL;

const openLink = async (url = DEFAULT_URL) => {
  const iframe = document.getElementById("preview");
  if (iframe) {
    iframe.src = url;
  }
  currentUrl = url;
  updateSidebarActiveState();

  saveState();
};

const updateSidebarActiveState = () => {
  const links = document.querySelectorAll("#sidebar a");
  links.forEach((link) => {
    if (link.href.includes(currentUrl)) {
      link.classList.add("active");
      link.classList.remove("un-active");
    } else {
      link.classList.add("un-active");
      link.classList.remove("active");
    }
  });
};

const createSidebarItems = (items) => {
  const sidebar = document.getElementById("sidebar");
  sidebar.innerHTML = "";
  items.forEach((item) => {
    const link = document.createElement("a");
    link.href = item.url;
    link.title = item.title;
    link.className = "un-active";
    link.innerHTML = `<img src="${item.icon}" alt="${item.title}" />`;
    link.addEventListener("click", (e) => {
      e.preventDefault();
      openLink(item.url);
    });
    sidebar.appendChild(link);
  });
};

const saveState = () => {
  localStorage.setItem("currentUrl", currentUrl);
};

const loadState = () => {
  const savedUrl = localStorage.getItem("currentUrl");
  createSidebarItems(SIDEBAR_ITEMS);
  openLink(savedUrl || DEFAULT_URL);
};

document.addEventListener("DOMContentLoaded", () => {
  loadState();
});

window.addEventListener("message", (event) => {
  const { type, productUrl } = event.data || {};

  if (type === "START_AUTOMATION") {
    console.log("Automation requested for:", productUrl);

    chrome.runtime.sendMessage({
      type: "START_AUTOMATION",
      productUrl,
    });
  }
});
