# Configuration file for Marktplaats automation
# Copy this file to config.py and fill in your actual values

# Marktplaats login credentials
EMAIL = 'your_email@example.com'
PASSWORD = 'your_password'

# Chrome profile directory
# Option 1: Use your existing Chrome profile (requires closing Chrome before running)
# Windows example: r'C:\Users\YOUR_USERNAME\AppData\Local\Google\Chrome\User Data'
# Linux example: '/home/YOUR_USERNAME/.config/google-chrome'
# Option 2: Use a separate profile for automation (recommended, no need to close Chrome)
# Windows example: r'C:\git\marktplaats\chrome-profile'
# Linux example: '/path/to/marktplaats/chrome-profile'
CHROME_USER_DATA_DIR = r'C:\git\marktplaats\chrome-profile'

# Chrome options
HEADLESS_MODE = False  # Set to True to run without visible browser window
WINDOW_SIZE = '1920,1080'  # Window size for headless mode

# Browser cookies for API authentication (optional)
# Used by scrape_categories.py to access Marktplaats API
# To obtain: Open Chrome > F12 > Application tab > Cookies > marktplaats.nl
# Copy the entire Cookie header value (all cookies as one string)
BROWSER_COOKIES = None  # Replace with your cookie string
