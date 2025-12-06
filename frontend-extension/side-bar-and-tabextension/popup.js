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

// Supabase configuration - will be loaded from storage
let supabaseClient = null;
let supabaseUrl = null;
let supabaseKey = null;

// View management - will be initialized after DOM loads
let views = {};

function initViews() {
  views = {
    auth: document.getElementById('auth-view'),
    choice: document.getElementById('choice-view'),
    processing: document.getElementById('processing-view'),
    completion: document.getElementById('completion-view'),
  };
}

function showView(viewName) {
  // Make sure views are initialized
  if (!views.auth) {
    initViews();
  }
  
  Object.values(views).forEach(view => {
    if (view) view.classList.remove('active');
  });
  
  if (views[viewName]) {
    views[viewName].classList.add('active');
  } else {
    console.error('View not found:', viewName, 'Available views:', Object.keys(views));
    // Fallback: show auth view if view not found
    if (views.auth) {
      views.auth.classList.add('active');
    }
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

// Update user info display
function updateUserInfo(user) {
  const userInfo = document.getElementById('user-info');
  const userEmail = document.getElementById('user-email');
  
  if (user && userInfo && userEmail) {
    userEmail.textContent = user.email || 'User';
    userInfo.style.display = 'flex';
  }
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
  // This step waits for backend to scrape the job posting
  activateStep('step-1');
  
  // Wait for backend response (this is where scraping happens)
  let waited = 0;
  const maxWait = 60000; // 60 seconds max
  while (!window.backendResponseReceived && waited < maxWait) {
    await new Promise(resolve => setTimeout(resolve, 100));
    waited += 100;
  }
  
  await animateProgress(0, 25, 1500, (value) => {
    progressFill.style.width = value + '%';
    matchScoreValue = Math.floor(value * 0.8);
    matchScore.textContent = matchScoreValue + '%';
  });
  
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
  // Check if user is authenticated first
  if (!supabaseClient) {
    const initialized = await initSupabase();
    if (!initialized) {
      alert('Please configure Supabase credentials in config.js first.');
      showView('auth');
      return;
    }
  }

  // Check authentication status
  const { data: { session } } = await supabaseClient.auth.getSession();
  if (!session) {
    alert('Please sign in to use this feature.');
    showView('auth');
    return;
  }

  // Get user_id from session
  const userId = session.user?.id;
  if (!userId) {
    alert('Error: Could not get user ID. Please sign in again.');
    showView('auth');
    return;
  }

  const tab = await getCurrentTab();
  
  if (!tab || !tab.url) {
    alert('Error: Could not get current tab URL. Please try again.');
    return;
  }
  
  // Reset backend response flag
  window.backendResponseReceived = false;
  window.currentJobData = null;
  window.currentAIResponse = null;
  
  // Show processing view immediately
  showView('processing');
  
  // Start progress animation (will wait for backend during step 1)
  const progressPromise = simulateAIProcessing();
  
  // Send message to background script to start AI processing
  chrome.runtime.sendMessage({
    type: 'START_JOB_APPLICATION',
    tabUrl: tab.url,
    tabId: tab.id,
    userId: userId, // Pass user_id to fetch resume from Supabase
  }, (response) => {
    if (chrome.runtime.lastError) {
      console.error('Error:', chrome.runtime.lastError);
      alert('Error: ' + chrome.runtime.lastError.message + '\n\nMake sure the backend API server is running:\npython backend/api_server.py');
      showView('choice');
      return;
    }
    
    if (response && response.success) {
      // Store the response
      window.currentJobData = response.job_data;
      window.currentAIResponse = response.ai_response;
      window.currentPdfPath = response.pdf_path; // Store PDF path for download
      window.backendResponseReceived = true;
      console.log('Backend processing completed successfully');
      console.log('PDF path stored:', window.currentPdfPath);
    } else {
      // Show error
      const errorMsg = response?.error || 'Unknown error occurred';
      console.error('Backend error:', errorMsg);
      alert('Error: ' + errorMsg);
      showView('choice');
    }
  });
});

document.getElementById('open-sidebar-btn').addEventListener('click', async () => {
  // Check if user is authenticated first
  if (!supabaseClient) {
    const initialized = await initSupabase();
    if (!initialized) {
      alert('Please configure Supabase credentials in config.js first.');
      showView('auth');
      return;
    }
  }

  // Check authentication status
  const { data: { session } } = await supabaseClient.auth.getSession();
  if (!session) {
    alert('Please sign in to use this feature.');
    showView('auth');
    return;
  }

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
  // Check if we have a PDF path from the backend response
  if (!window.currentPdfPath) {
    alert('No resume PDF available. Please run the job application process first.');
    return;
  }
  
  // Send download request to background script with PDF path
  chrome.runtime.sendMessage({
    type: 'DOWNLOAD_RESUME',
    pdf_path: window.currentPdfPath,
  }, (response) => {
    if (chrome.runtime.lastError) {
      console.error('Error:', chrome.runtime.lastError);
      alert('Error downloading resume: ' + chrome.runtime.lastError.message);
      return;
    }
    
    if (response && response.success) {
      console.log('Resume download initiated');
    } else {
      const errorMsg = response?.error || 'Unknown error occurred';
      console.error('Download error:', errorMsg);
      alert('Error downloading resume: ' + errorMsg);
    }
  });
});

document.getElementById('view-resume-btn').addEventListener('click', () => {
  // TODO: Implement preview functionality
  chrome.runtime.sendMessage({
    type: 'VIEW_RESUME',
  });
  
  // Show notification or feedback
  alert('Resume preview will be implemented with backend integration!');
});

// Initialize Supabase client
async function initSupabase() {
  // Check if Supabase is loaded
  if (typeof window.supabase === 'undefined') {
    console.error('Supabase library not loaded');
    return false;
  }

  // First, try to get from config.js (like .env.local in web app)
  console.log('Checking SUPABASE_CONFIG:', {
    exists: typeof window.SUPABASE_CONFIG !== 'undefined',
    url: window.SUPABASE_CONFIG?.url,
    anonKey: window.SUPABASE_CONFIG?.anonKey ? 'present (' + window.SUPABASE_CONFIG.anonKey.substring(0, 20) + '...)' : 'missing',
    urlValid: window.SUPABASE_CONFIG?.url && window.SUPABASE_CONFIG.url !== 'YOUR_SUPABASE_URL_HERE',
    keyValid: window.SUPABASE_CONFIG?.anonKey && window.SUPABASE_CONFIG.anonKey !== 'YOUR_SUPABASE_ANON_KEY_HERE'
  });

  if (typeof window.SUPABASE_CONFIG !== 'undefined' && 
      window.SUPABASE_CONFIG.url && 
      window.SUPABASE_CONFIG.url !== 'YOUR_SUPABASE_URL_HERE' &&
      window.SUPABASE_CONFIG.anonKey && 
      window.SUPABASE_CONFIG.anonKey !== 'YOUR_SUPABASE_ANON_KEY_HERE') {
    supabaseUrl = window.SUPABASE_CONFIG.url;
    supabaseKey = window.SUPABASE_CONFIG.anonKey;
    
    console.log('Initializing Supabase with config from config.js');
    console.log('URL:', supabaseUrl);
    console.log('Key present:', !!supabaseKey);
    
    try {
      supabaseClient = window.supabase.createClient(supabaseUrl, supabaseKey, {
        auth: {
          persistSession: false, // We'll handle session persistence manually
          autoRefreshToken: true,
          detectSessionInUrl: false,
        },
      });
      console.log('Supabase client created successfully');
      // Save to storage for future use
      await chrome.storage.sync.set({ supabaseUrl, supabaseKey });
      return true;
    } catch (error) {
      console.error('Error creating Supabase client:', error);
      return false;
    }
  } else {
    console.log('SUPABASE_CONFIG check:', {
      exists: typeof window.SUPABASE_CONFIG !== 'undefined',
      url: window.SUPABASE_CONFIG?.url,
      anonKey: window.SUPABASE_CONFIG?.anonKey ? 'present' : 'missing'
    });
  }

  // Fallback: Get Supabase credentials from storage (if previously set)
  const result = await chrome.storage.sync.get(['supabaseUrl', 'supabaseKey']);
  
  if (result.supabaseUrl && result.supabaseKey) {
    supabaseUrl = result.supabaseUrl;
    supabaseKey = result.supabaseKey;
    supabaseClient = window.supabase.createClient(supabaseUrl, supabaseKey, {
      auth: {
        persistSession: false, // We'll handle session persistence manually
        autoRefreshToken: true,
        detectSessionInUrl: false,
      },
    });
    return true;
  }
  
  // If not configured, show error
  console.error('Supabase credentials not configured. Please update config.js with your Supabase URL and anon key from web/.env.local');
  return false;
}

// Check authentication status
async function checkAuth() {
  if (!supabaseClient) {
    const initialized = await initSupabase();
    if (!initialized) {
      // Show error message in auth view
      const authView = document.getElementById('auth-view');
      if (authView) {
        const errorMsg = document.createElement('div');
        errorMsg.className = 'error-message';
        errorMsg.style.display = 'block';
        errorMsg.style.marginBottom = '16px';
        errorMsg.innerHTML = '⚠️ Supabase not configured. Please update <code>config.js</code> with your credentials from <code>web/.env.local</code>';
        const authContainer = authView.querySelector('.auth-container');
        if (authContainer && !authContainer.querySelector('.error-message:not(#signin-error):not(#signup-error)')) {
          authContainer.insertBefore(errorMsg, authContainer.querySelector('.auth-tabs'));
        }
      }
      showView('auth');
      return false;
    }
  }

  try {
    const { data: { session }, error } = await supabaseClient.auth.getSession();
    
    if (error) {
      console.error('Auth error:', error);
      showView('auth');
      return false;
    }

    if (session) {
      // User is authenticated
      showView('choice');
      // Update user info display
      updateUserInfo(session.user);
      return true;
    } else {
      // No session, show auth view
      showView('auth');
      return false;
    }
  } catch (error) {
    console.error('Error checking auth:', error);
    showView('auth');
    return false;
  }
}

// Sign in handler
async function handleSignIn(email, password) {
  const errorEl = document.getElementById('signin-error');
  const submitBtn = document.getElementById('signin-submit');
  
  console.log('=== handleSignIn called ===');
  console.log('Email:', email);
  console.log('supabaseClient:', supabaseClient ? 'initialized' : 'not initialized');
  
  errorEl.style.display = 'none';
  submitBtn.disabled = true;
  submitBtn.textContent = 'Signing in...';

  // Make sure Supabase is initialized
  if (!supabaseClient) {
    console.log('Supabase client not initialized, initializing...');
    const initialized = await initSupabase();
    if (!initialized) {
      console.error('Failed to initialize Supabase');
      errorEl.textContent = 'Supabase not configured. Please check config.js';
      errorEl.style.display = 'block';
      submitBtn.disabled = false;
      submitBtn.textContent = 'Sign In';
      return;
    }
    console.log('Supabase initialized successfully');
  }

  try {
    console.log('Attempting to sign in with Supabase...');
    console.log('Supabase URL:', supabaseClient.supabaseUrl);
    
    // Add timeout to prevent hanging
    const signInPromise = supabaseClient.auth.signInWithPassword({
      email,
      password,
    });
    
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error('Sign in request timed out. Please check your internet connection and try again.')), 10000);
    });
    
    const { data, error } = await Promise.race([signInPromise, timeoutPromise]);

    console.log('Sign in response:', { 
      hasData: !!data, 
      hasError: !!error,
      hasSession: !!data?.session,
      hasUser: !!data?.user,
      errorMessage: error?.message,
      errorStatus: error?.status
    });

    if (error) {
      console.error('Sign in error details:', {
        message: error.message,
        status: error.status,
        name: error.name,
        fullError: error
      });
      
      // Provide more helpful error messages
      let errorMessage = error.message || 'Failed to sign in';
      if (error.status === 400) {
        errorMessage = 'Invalid email or password. Please check your credentials.';
      } else if (error.status === 429) {
        errorMessage = 'Too many requests. Please wait a moment and try again.';
      } else if (error.message?.includes('network') || error.message?.includes('fetch')) {
        errorMessage = 'Network error. Please check your internet connection and try again.';
      }
      
      throw new Error(errorMessage);
    }

    if (data.session) {
      console.log('Sign in successful! Saving session...');
      // Save session to chrome.storage for persistence
      await chrome.storage.local.set({
        supabaseSession: data.session,
        supabaseUser: data.user,
      });
      console.log('Session saved to chrome.storage');

      // Show main view
      console.log('Switching to choice view...');
      showView('choice');
      updateUserInfo(data.user);
      updateSiteInfo();
      console.log('Sign in complete!');
    } else {
      console.error('No session in response data');
      throw new Error('No session received from server. Please try again.');
    }
  } catch (error) {
    console.error('Sign in failed:', error);
    const errorMessage = error.message || 'Failed to sign in. Please check your credentials and try again.';
    errorEl.textContent = errorMessage;
    errorEl.style.display = 'block';
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Sign In';
    console.log('Sign in handler finished');
  }
}

// Sign up handler
async function handleSignUp(name, email, password, confirmPassword) {
  const errorEl = document.getElementById('signup-error');
  const submitBtn = document.getElementById('signup-submit');
  
  errorEl.style.display = 'none';
  submitBtn.disabled = true;
  submitBtn.textContent = 'Creating account...';

  // Validate passwords match
  if (password !== confirmPassword) {
    errorEl.textContent = 'Passwords do not match';
    errorEl.style.display = 'block';
    submitBtn.disabled = false;
    submitBtn.textContent = 'Sign Up';
    return;
  }

  if (password.length < 6) {
    errorEl.textContent = 'Password must be at least 6 characters';
    errorEl.style.display = 'block';
    submitBtn.disabled = false;
    submitBtn.textContent = 'Sign Up';
    return;
  }

  // Make sure Supabase is initialized
  if (!supabaseClient) {
    const initialized = await initSupabase();
    if (!initialized) {
      errorEl.textContent = 'Supabase not configured. Please check config.js';
      errorEl.style.display = 'block';
      submitBtn.disabled = false;
      submitBtn.textContent = 'Sign Up';
      return;
    }
  }

  try {
    const { data, error } = await supabaseClient.auth.signUp({
      email,
      password,
      options: {
        data: {
          name: name,
        },
      },
    });

    if (error) throw error;

    if (data.user) {
      // Update profile with name
      await supabaseClient
        .from('profiles')
        .upsert({
          id: data.user.id,
          name: name,
          updated_at: new Date().toISOString()
        }, {
          onConflict: 'id'
        });

      // Save session if available
      if (data.session) {
        await chrome.storage.local.set({
          supabaseSession: data.session,
          supabaseUser: data.user,
        });
        showView('choice');
        updateUserInfo(data.user);
        updateSiteInfo();
      } else {
        // Email confirmation required
        errorEl.innerHTML = 'Account created! Please check your email to confirm your account.';
        errorEl.style.display = 'block';
        errorEl.style.color = '#4ade80';
      }
    }
  } catch (error) {
    errorEl.textContent = error.message || 'Failed to create account';
    errorEl.style.display = 'block';
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Sign Up';
  }
}

// Sign out handler
async function handleSignOut() {
  if (supabaseClient) {
    await supabaseClient.auth.signOut();
  }
  await chrome.storage.local.remove(['supabaseSession', 'supabaseUser']);
  showView('auth');
}

// Restore session from storage
async function restoreSession() {
  // First, make sure Supabase is initialized
  if (!supabaseClient) {
    const initialized = await initSupabase();
    if (!initialized) {
      return false;
    }
  }

  const result = await chrome.storage.local.get(['supabaseSession', 'supabaseUser']);
  
  if (result.supabaseSession && supabaseClient) {
    try {
      // Set the session - use refresh_token if available
      const sessionData = result.supabaseSession;
      const { data, error } = await supabaseClient.auth.setSession({
        access_token: sessionData.access_token,
        refresh_token: sessionData.refresh_token,
      });
      
      if (error) {
        // Session expired or invalid
        await chrome.storage.local.remove(['supabaseSession', 'supabaseUser']);
        return false;
      }

      if (data.session) {
        // Update stored session
        await chrome.storage.local.set({
          supabaseSession: data.session,
          supabaseUser: data.user,
        });
        updateUserInfo(data.user);
        return true;
      }
    } catch (error) {
      console.error('Error restoring session:', error);
      await chrome.storage.local.remove(['supabaseSession', 'supabaseUser']);
      return false;
    }
  }
  
  return false;
}

// Track if we've initialized to prevent double initialization
let isInitialized = false;

// Initialize - use window.onload to ensure all scripts are loaded
window.addEventListener('load', async () => {
  if (isInitialized) return;
  console.log('=== window.load fired ===');
  isInitialized = true;
  await initializeApp();
});

// Also try DOMContentLoaded as fallback (for faster popup opening)
document.addEventListener('DOMContentLoaded', async () => {
  if (isInitialized) return;
  console.log('=== DOMContentLoaded fired ===');
  // Wait a bit for scripts to load, then initialize
  setTimeout(async () => {
    if (!isInitialized) {
      isInitialized = true;
      await initializeApp();
    }
  }, 100);
});

async function initializeApp() {
  // Initialize views first
  initViews();
  
  // Show auth view by default (will be changed if user is authenticated)
  showView('auth');
  
  // Check what we have
  console.log('=== Checking for scripts ===');
  console.log('window.supabase:', typeof window.supabase !== 'undefined' ? '✓ Loaded' : '✗ Not loaded');
  console.log('window.SUPABASE_CONFIG:', typeof window.SUPABASE_CONFIG !== 'undefined' ? '✓ Loaded' : '✗ Not loaded');
  
  // Verify scripts loaded
  if (typeof window.SUPABASE_CONFIG === 'undefined') {
    console.error('⚠️ config.js did not load!');
    console.error('Possible causes:');
    console.error('1. File path is incorrect');
    console.error('2. File has JavaScript syntax errors');
    console.error('3. Chrome extension CSP is blocking it');
    console.error('4. File permissions issue');
  }
  
  if (typeof window.supabase === 'undefined') {
    console.error('⚠️ Supabase library did not load!');
    console.error('Make sure supabase-js.min.js is in the extension directory');
  }
  
  if (window.SUPABASE_CONFIG) {
    console.log('SUPABASE_CONFIG.url:', window.SUPABASE_CONFIG.url || 'MISSING');
    console.log('SUPABASE_CONFIG.anonKey:', window.SUPABASE_CONFIG.anonKey ? '✓ Present (' + window.SUPABASE_CONFIG.anonKey.substring(0, 20) + '...)' : '✗ Missing');
  }
  
  // Wait for scripts to load if not already loaded
  if (typeof window.supabase === 'undefined' || typeof window.SUPABASE_CONFIG === 'undefined') {
    console.log('Waiting for scripts to load...');
    await new Promise(resolve => {
      let attempts = 0;
      const maxAttempts = 50; // 5 seconds
      const checkInterval = setInterval(() => {
        attempts++;
        const supabaseLoaded = typeof window.supabase !== 'undefined';
        const configLoaded = typeof window.SUPABASE_CONFIG !== 'undefined';
        
        if (attempts % 10 === 0 || (supabaseLoaded && configLoaded)) { // Log every 10 attempts or when loaded
          console.log(`Attempt ${attempts}/${maxAttempts}: supabase=${supabaseLoaded}, config=${configLoaded}`);
        }
        
        if ((supabaseLoaded && configLoaded) || attempts >= maxAttempts) {
          clearInterval(checkInterval);
          console.log(`Scripts check complete: supabase=${supabaseLoaded}, config=${configLoaded}`);
          resolve();
        }
      }, 100);
    });
  }

  // Final check
  console.log('=== Final check ===');
  console.log('window.supabase:', typeof window.supabase !== 'undefined' ? '✓ Loaded' : '✗ Not loaded');
  console.log('window.SUPABASE_CONFIG:', typeof window.SUPABASE_CONFIG !== 'undefined' ? '✓ Loaded' : '✗ Not loaded');
  
  if (window.SUPABASE_CONFIG) {
    console.log('SUPABASE_CONFIG.url:', window.SUPABASE_CONFIG.url || 'MISSING');
    console.log('SUPABASE_CONFIG.anonKey:', window.SUPABASE_CONFIG.anonKey ? '✓ Present (' + window.SUPABASE_CONFIG.anonKey.substring(0, 20) + '...)' : '✗ Missing');
  } else {
    console.error('✗ SUPABASE_CONFIG is still not defined!');
    console.error('Troubleshooting:');
    console.error('1. Check if config.js file exists in the extension directory');
    console.error('2. Check Network tab to see if config.js is loading (status 200)');
    console.error('3. Check Console for any JavaScript errors in config.js');
    console.error('4. Verify config.js has correct syntax (no missing quotes, brackets, etc.)');
    console.error('5. Try reloading the extension completely');
  }

  // Initialize Supabase
  const initialized = await initSupabase();
  if (!initialized) {
    console.error('Failed to initialize Supabase');
    console.log('Debug info:', {
      supabaseLoaded: typeof window.supabase !== 'undefined',
      configExists: typeof window.SUPABASE_CONFIG !== 'undefined',
      configUrl: window.SUPABASE_CONFIG?.url,
      configKey: window.SUPABASE_CONFIG?.anonKey ? 'present' : 'missing'
    });
    
    // Keep showing auth view with error message
    const authView = document.getElementById('auth-view');
    if (authView) {
      // Remove any existing error messages
      const existingErrors = authView.querySelectorAll('.error-message:not(#signin-error):not(#signup-error)');
      existingErrors.forEach(err => err.remove());
      
      const errorMsg = document.createElement('div');
      errorMsg.className = 'error-message';
      errorMsg.style.display = 'block';
      errorMsg.style.marginBottom = '16px';
      errorMsg.innerHTML = '⚠️ Supabase not configured. Please check config.js and reload the extension.<br><small>Check browser console (F12) for details.</small>';
      const authContainer = authView.querySelector('.auth-container');
      if (authContainer) {
        const authTabs = authContainer.querySelector('.auth-tabs');
        if (authTabs) {
          authContainer.insertBefore(errorMsg, authTabs);
        } else {
          authContainer.appendChild(errorMsg);
        }
      }
    }
    return; // Stop here if Supabase not initialized
  }
  
  // Try to restore session
  const hasSession = await restoreSession();
  
  // Check auth status (this will show the appropriate view)
  const isAuthenticated = await checkAuth();
  
  if (isAuthenticated || hasSession) {
    updateSiteInfo();
  } else {
    // Make sure auth view is shown if not authenticated
    showView('auth');
  }

  // Set up event listeners
  setupEventListeners();
}

function setupEventListeners() {
  // Auth tab switching
  document.querySelectorAll('.auth-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const tabName = tab.dataset.tab;
      
      // Update active tab
      document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      
      // Update active form
      document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
      document.getElementById(`${tabName}-form`).classList.add('active');
      
      // Clear errors
      document.querySelectorAll('.error-message').forEach(e => {
        e.style.display = 'none';
        e.textContent = '';
      });
    });
  });

  // Sign in form handler
  const signinForm = document.getElementById('signin-form-element');
  if (signinForm) {
    console.log('Sign in form found, adding event listener');
    signinForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      console.log('Sign in form submitted');
      
      // Make sure Supabase is initialized before signing in
      if (!supabaseClient) {
        console.log('Supabase client not initialized, initializing...');
        const initialized = await initSupabase();
        if (!initialized) {
          console.error('Failed to initialize Supabase');
          const errorEl = document.getElementById('signin-error');
          if (errorEl) {
            errorEl.textContent = 'Supabase not configured. Please check config.js and reload the extension.';
            errorEl.style.display = 'block';
          }
          return;
        }
        console.log('Supabase initialized successfully');
      }
      
      const email = document.getElementById('signin-email').value;
      const password = document.getElementById('signin-password').value;
      
      if (!email || !password) {
        console.error('Email or password is empty');
        const errorEl = document.getElementById('signin-error');
        if (errorEl) {
          errorEl.textContent = 'Please enter both email and password';
          errorEl.style.display = 'block';
        }
        return;
      }
      
      console.log('Calling handleSignIn...');
      await handleSignIn(email, password);
    });
  } else {
    console.error('Sign in form not found!');
  }

  // Sign up form handler
  const signupForm = document.getElementById('signup-form-element');
  if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      // Make sure Supabase is initialized before signing up
      if (!supabaseClient) {
        const initialized = await initSupabase();
        if (!initialized) {
          const errorEl = document.getElementById('signup-error');
          if (errorEl) {
            errorEl.textContent = 'Supabase not configured. Please check config.js and reload the extension.';
            errorEl.style.display = 'block';
          }
          return;
        }
      }
      
      const name = document.getElementById('signup-name').value;
      const email = document.getElementById('signup-email').value;
      const password = document.getElementById('signup-password').value;
      const confirmPassword = document.getElementById('signup-confirm-password').value;
      await handleSignUp(name, email, password, confirmPassword);
    });
  }

  // Sign out button handler
  const signOutBtn = document.getElementById('sign-out-btn');
  if (signOutBtn) {
    signOutBtn.addEventListener('click', async () => {
      await handleSignOut();
    });
  }

  // Update site info when tab changes (if popup stays open)
  chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete') {
      updateSiteInfo();
    }
  });
}

