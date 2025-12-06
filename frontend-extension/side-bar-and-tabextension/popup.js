// Job site detection patterns
const JOB_SITE_PATTERNS = [
  /linkedin\.com\/jobs/,
  /indeed\.com/,
  /glassdoor\.com/,
  /monster\.com/,
  /ziprecruiter\.com/,
  /careerbuilder\.com/,
  /dice\.com/,
  /angel\.co/,
  /stackoverflow\.com\/jobs/,
  /github\.com\/.*jobs/,
  /remoteok\.io/,
  /weworkremotely\.com/,
  /jobs\.lever\.co/,
  /greenhouse\.io/,
  /workday\.com/,
];

// View management
const views = {
  choice: document.getElementById('choice-view'),
  processing: document.getElementById('processing-view'),
  completion: document.getElementById('completion-view'),
};

function showView(viewName) {
  Object.values(views).forEach(view => view.classList.remove('active'));
  if (views[viewName]) {
    views[viewName].classList.add('active');
  }
}

// Get current tab URL
async function getCurrentTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

// Check if current site is a job site
function isJobSite(url) {
  if (!url) return false;
  return JOB_SITE_PATTERNS.some(pattern => pattern.test(url));
}

// Update UI with current site info
async function updateSiteInfo() {
  const tab = await getCurrentTab();
  const urlElement = document.getElementById('current-url');
  const jobBadge = document.getElementById('job-badge');
  
  if (tab && tab.url) {
    try {
      const url = new URL(tab.url);
      const domain = url.hostname.replace('www.', '');
      urlElement.textContent = domain;
      
      // Show job detection badge if on a job site
      if (isJobSite(tab.url)) {
        jobBadge.style.display = 'flex';
      } else {
        jobBadge.style.display = 'none';
      }
    } catch (e) {
      urlElement.textContent = 'Unknown site';
    }
  } else {
    urlElement.textContent = 'No active tab';
  }
}

// Simulate AI processing with progress updates
async function simulateAIProcessing() {
  showView('processing');
  
  const progressFill = document.getElementById('progress-fill');
  const matchScore = document.getElementById('match-score');
  const keywordsMatched = document.getElementById('keywords-matched');
  const steps = ['step-1', 'step-2', 'step-3', 'step-4'];
  
  let currentStep = 0;
  let progress = 0;
  let matchScoreValue = 0;
  let keywordsValue = 0;
  
  // Step 1: Analyzing job description (0-25%)
  await animateProgress(0, 25, 1500, (value) => {
    progressFill.style.width = value + '%';
    matchScoreValue = Math.floor(value * 0.8);
    matchScore.textContent = matchScoreValue + '%';
  });
  activateStep('step-1');
  
  // Step 2: Tailoring resume content (25-50%)
  await animateProgress(25, 50, 2000, (value) => {
    progressFill.style.width = value + '%';
    matchScoreValue = Math.floor(value * 0.9);
    matchScore.textContent = matchScoreValue + '%';
    keywordsValue = Math.floor((value - 25) * 0.96);
    keywordsMatched.textContent = keywordsValue;
  });
  activateStep('step-2');
  
  // Step 3: Optimizing keywords (50-75%)
  await animateProgress(50, 75, 1800, (value) => {
    progressFill.style.width = value + '%';
    matchScoreValue = Math.floor(value * 0.95);
    matchScore.textContent = matchScoreValue + '%';
    keywordsValue = Math.floor((value - 25) * 0.96);
    keywordsMatched.textContent = keywordsValue;
  });
  activateStep('step-3');
  
  // Step 4: Finalizing resume (75-100%)
  await animateProgress(75, 100, 1500, (value) => {
    progressFill.style.width = value + '%';
    matchScoreValue = Math.min(95, Math.floor(value * 0.95));
    matchScore.textContent = matchScoreValue + '%';
    keywordsValue = Math.min(24, Math.floor((value - 25) * 0.96));
    keywordsMatched.textContent = keywordsValue;
  });
  activateStep('step-4');
  
  // Wait a bit before showing completion
  await new Promise(resolve => setTimeout(resolve, 500));
  
  showCompletion();
}

function animateProgress(start, end, duration, callback) {
  return new Promise((resolve) => {
    const startTime = Date.now();
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const value = start + (end - start) * easeInOutCubic(progress);
      callback(value);
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        resolve();
      }
    };
    animate();
  });
}

function easeInOutCubic(t) {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

function activateStep(stepId) {
  document.getElementById(stepId).classList.add('active');
}

function showCompletion() {
  showView('completion');
  
  // Set final stats
  document.getElementById('final-match-score').textContent = '95%';
  document.getElementById('final-keywords').textContent = '24';
}

// Handle button clicks
document.getElementById('apply-job-btn').addEventListener('click', async () => {
  const tab = await getCurrentTab();
  
  // TODO: Send message to background script to start AI processing
  // For now, we'll simulate the process
  chrome.runtime.sendMessage({
    type: 'START_JOB_APPLICATION',
    tabUrl: tab.url,
    tabId: tab.id,
  });
  
  simulateAIProcessing();
});

document.getElementById('open-sidebar-btn').addEventListener('click', async () => {
  // Get current tab to get windowId
  const tab = await getCurrentTab();
  
  // Open sidebar panel
  chrome.runtime.sendMessage({
    type: 'OPEN_SIDEBAR',
    tabId: tab.id,
  }, (response) => {
    // Close popup after sidebar opens
    if (response && response.success) {
      window.close();
    }
  });
});

document.getElementById('back-to-choice-btn').addEventListener('click', () => {
  showView('choice');
  // Reset progress
  document.getElementById('progress-fill').style.width = '0%';
  document.querySelectorAll('.step').forEach(step => {
    step.classList.remove('active');
  });
});

document.getElementById('download-resume-btn').addEventListener('click', () => {
  // TODO: Implement download functionality
  chrome.runtime.sendMessage({
    type: 'DOWNLOAD_RESUME',
  });
  
  // Show notification or feedback
  alert('Resume download will be implemented with backend integration!');
});

document.getElementById('view-resume-btn').addEventListener('click', () => {
  // TODO: Implement preview functionality
  chrome.runtime.sendMessage({
    type: 'VIEW_RESUME',
  });
  
  // Show notification or feedback
  alert('Resume preview will be implemented with backend integration!');
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  updateSiteInfo();
  
  // Update site info when tab changes (if popup stays open)
  chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete') {
      updateSiteInfo();
    }
  });
});

