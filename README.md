# Marktplaats Manager

A Python automation tool for managing Marktplaats accounts with large numbers of ads (300+). This tool automatically checks for expired ads and reposts them using Selenium web automation.

> **⚠️ Important:** Always use valid category paths from [categories/categorieen.txt](categories/categorieen.txt). Do not create custom categories - they must match exactly!

## Features

- **Automatic Reposting**: Monitors expired ads and automatically reposts them
- **Bulk Ad Management**: Handles 300+ ads efficiently
- **Image Processing**: Automatically rotates images based on EXIF orientation data
- **Category Management**: Organizes ads into proper Marktplaats categories
- **Shipping Integration**: Supports PostNL shipping options
- **Cookie & Session Handling**: Manages login sessions and cookies
- **Headless Operation**: Can run without a visible browser window

## Prerequisites

- Python 3.x
- Google Chrome browser
  - ChromeDriver is automatically managed by Selenium (no manual installation needed)

## Installation

### 1. Create a Virtual Environment (Recommended)

It's recommended to use a virtual environment to isolate project dependencies:

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

### 3. Configure Settings

Copy the example configuration file and edit it with your settings:

```bash
cp config.example.py config.py
```

Edit `config.py` and set:
- **EMAIL**: Your Marktplaats login email
- **PASSWORD**: Your Marktplaats password
- **CHROME_USER_DATA_DIR**: Path to Chrome profile (use separate automation profile recommended)
- **BROWSER_COOKIES** (optional): For category scraper API access

#### How to Get Browser Cookies (for scrape_categories.py)

The category scraper needs browser cookies to access the Marktplaats API:

1. Open Chrome and log in to Marktplaats
2. Press `F12` to open DevTools
3. Go to **Application** tab
4. In the left sidebar, expand **Cookies** and click **https://www.marktplaats.nl**
5. Look for the **Cookie** value (or copy individual cookies)
6. Right-click on any cookie row > **Show Cookies** or manually copy all cookie values
7. Format as: `cookie1=value1; cookie2=value2; cookie3=value3`
8. Paste the entire string into `config.py` as `BROWSER_COOKIES`

**Alternative method:**
1. In DevTools, go to **Network** tab
2. Refresh the page or navigate to any Marktplaats page
3. Click on any request to marktplaats.nl
4. In **Headers** section, find **Request Headers**
5. Copy the entire **Cookie:** header value
6. Paste into `config.py` as `BROWSER_COOKIES`

## Project Structure

```
marktplaats-manager/
├── automation.py           # Main automation script
├── requirements.txt        # Python dependencies
├── config.example.py       # Example configuration file
├── config.py              # Your configuration (create from example)
├── .gitignore             # Git ignore file
├── README.md              # This file
├── .venv/                 # Virtual environment (create this)
├── Example ad - HP Z600 workstation/
│   ├── Beschrijving.txt   # Ad description
│   ├── Categorie.txt      # Category and pricing info
│   └── photos/             # Product images
└── ads/                   # Folder for your ads (create this)
    └── [Your Ad Name]/
        ├── Beschrijving.txt
        ├── Categorie.txt
        └── photos/
            ├── image1.jpg
            ├── image2.jpg
            └── ...
```

## Setup

### 1. Activate Virtual Environment

Before running the script, make sure to activate your virtual environment:

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 2. Create Configuration File

Copy the example configuration file and edit it with your settings:

**Windows:**
```bash
copy config.example.py config.py
```

**Linux/Mac:**
```bash
cp config.example.py config.py
```

Then edit `config.py` and set:
- `EMAIL`: Your Marktplaats email address
- `PASSWORD`: Your Marktplaats password
- `CHROME_USER_DATA_DIR`: Path to Chrome profile directory
  - **Option 1** (existing profile): `r'C:\Users\YOUR_USERNAME\AppData\Local\Google\Chrome\User Data'` - Requires closing Chrome
  - **Option 2** (separate profile - recommended): `r'C:\git\marktplaats\chrome-profile'` - No need to close Chrome
- `HEADLESS_MODE`: Set to `True` to run without visible browser (optional)

### 4. Create Ad Folders

Create a folder structure for each ad in the `ads/` directory:

```
ads/
└── My Product Name/
    ├── index.txt          # Category + description combined
    └── photos/
        ├── photo1.jpg
        ├── photo2.jpg
        └── photo3.jpg
```

#### Quick Workflow with AI Assistant

**💡 Tip:** If you're using GitHub Copilot or similar AI assistant:

1. Take photos of your book (cover, back, any metadata/notes)
2. Drag the photos into the AI chat
3. Simply ask: **"create an ad 19.6 13 1.3 170"** (where the numbers correspond to the height, width, thickness in cm, and weight in grams)
4. The AI will create the ad folder and `index.txt` automatically
5. Move your photos to the generated `photos/` folder
6. Run `python automation.py` to post!

This workflow is especially efficient for books where you can photograph weight/dimensions notes alongside the book itself.

## Ad Configuration

### index.txt (Required)

Each ad requires an `index.txt` file with category information on the first line, followed by a separator line `---` (with newlines before and after), then the description:

**Format:**
```
Category1--Category2--Category3--Subject--Year--Condition--PriceType--Price--PackageSize
---
Description text goes here...
```

**Important:** The `---` separator must be on its own line (with newlines before and after) to avoid confusion with empty fields in the category line (which use `--`).

Example:
```
Boeken--Kunst en Cultuur--Beeldend--Beeldhouwkunst--1997--Gelezen--Bieden----Klein pakket
---
Camille Claudel - een vrouw
Door Anne Delbée
Uitgeverij: De Geus

Biografie over Camille Claudel, de getalenteerde maar vergeten beeldhouwster en kunstenares uit de late 19e eeuw. Dit boek vertelt het aangrijpende verhaal van haar leven, haar relatie met Auguste Rodin, en haar artistieke strijd in een door mannen gedomineerde kunstwereld.

Conditie: Gebruikt, in goede staat

Ophalen of verzenden mogelijk. Bied wat het boek voor jou waard is!
```

### Category Format

Format (double-dash separated):
```
Category1--Category2--Category3--Subject--Year--Condition--PriceType--Price--PackageSize
```

Example for Books:
```
Boeken--Kunst en Cultuur--Beeldend--Beeldhouwkunst--1997--Gelezen--Bieden----Klein pakket
```

Example for Computers:
```
Computers en Software--Computeronderdelen--Computerbehuizingen------Gebruikt--Vraagprijs--400,00--Gemiddeld pakket
```

**Field Descriptions:**

| Field | Description | Example Values | Notes |
|-------|-------------|----------------|-------|
| Category1 | Parent category | Boeken, Computers en Software | Required |
| Category2 | Child category | Kunst en Cultuur, Computeronderdelen | Required |
| Category3 | Grandchild category | Beeldend, Computerbehuizingen | Required |
| Subject | Category-specific subject | Beeldhouwkunst, Schilder- en Tekenkunst | Optional (books only) |
| Year | Publication/manufacture year | 1997, 2023 | Optional |
| Condition | Item condition | Gelezen, Nieuw, Gebruikt, Zo goed als nieuw | Optional |
| PriceType | Pricing method | Bieden, Vraagprijs, Gratis | Required |
| Price | Price amount | 400,00 (leave empty for Bieden) | Optional |
| PackageSize | Shipping package size | Klein pakket, Brievenbuspakje, Gemiddeld pakket, Groot pakket | Required for shipping |

**Package Size Options:**

- **Brievenbuspakje**: 0-2kg (fits in mailbox)
- **Klein pakket**: 0-3kg
- **Gemiddeld pakket**: 0-10kg
- **Groot pakket**: 10-23kg

**Book-Specific Subjects:**

When Category3 is "Beeldend", you can specify a subject ("Onderwerp") on the ad edit page:
- Beeldhouwkunst
- Grafische vormgeving
- Schilder- en Tekenkunst
- Overige onderwerpen


## How Selenium is Used in This Project

This project uses [Selenium](https://www.selenium.dev/) to automate browser actions for posting and managing ads on Marktplaats.nl. Selenium allows the script to control Google Chrome just like a human would, but fully automated from Python code.

### What Selenium Does in `automation.py`

1. **Browser Setup**: The script configures and launches a Chrome browser using Selenium's `webdriver.Chrome`, with options for user profile, headless mode, and more.
2. **Login Automation**: It navigates to Marktplaats.nl, handles cookie consent popups, and logs in using your credentials from `config.py`.
3. **Navigation**: Selenium is used to click through the Marktplaats interface, open your ad overview, and find which ads are already online.
4. **Ad Posting**: For each new ad (found in your `ads/` folder but not online), Selenium:
  - Navigates to the ad posting page
  - Fills in the ad title, selects the correct category using dropdowns, and uploads photos
  - Fills in the ad description and other fields (year, condition, price type, etc.)
  - Selects delivery and package options
  - Submits the ad
5. **Element Interaction**: The script uses Selenium's `find_element` and `find_elements` to locate page elements by XPath, CSS selectors, or IDs, and interacts with them (click, send_keys, select dropdowns) to mimic user actions.
6. **Waiting and Error Handling**: It uses `WebDriverWait` and `expected_conditions` to wait for elements to appear or become clickable, and handles exceptions if elements are not found or actions fail.

**Summary:** Selenium acts as a browser robot: it opens Chrome, logs in, navigates, fills forms, uploads files, and clicks buttons—just like a human, but fully automated from a Python script. This is useful for automating repetitive web tasks that don’t have an API.

---
## Usage

Run the automation script:

```bash
python automation.py
```

**What it does:**

1. Opens Chrome with your saved profile
2. Navigates to Marktplaats.nl
3. Handles cookie consent and login popups
4. Loads all your existing ads
5. Compares local ad folders with online ads
6. Reposts any ads that are not currently online
7. For each missing ad:
   - Creates a new listing
   - Uploads photos
   - Sets category and pricing
   - Configures shipping options
   - Publishes the ad

## Image Processing

The script automatically handles image orientation using EXIF data:
- Rotates images to correct orientation
- Converts to PNG format if needed
- Removes original files after conversion

## Advanced Configuration

### Headless Mode

To run without opening a browser window, set `HEADLESS_MODE = True` in your `config.py` file.

### Scheduling

For daily automation, set up a cron job (Linux) or Task Scheduler (Windows):

**Linux crontab:**
```bash
0 9 * * * /usr/bin/python3 /path/to/marktplaats/automation.py
```

**Windows Task Scheduler:**
```
Program: python.exe
Arguments: C:\git\marktplaats\automation.py
Trigger: Daily at 9:00 AM
```

## Troubleshooting

### Chrome Not Reachable / Session Not Created
- **Close ALL Chrome windows** before running the script
- Chrome's user data directory can only be used by one instance at a time
- Check Task Manager (Windows) / Activity Monitor (Mac) for lingering Chrome processes
- If Chrome is still running in the background, end the process and try again

### Login Issues
- Ensure your Chrome profile path is correct
- Check that credentials are properly set
- Try logging in manually first to save session

### Photo Upload Failures
- Check image file formats (JPG, PNG supported)
- Ensure photos are in the `photos/` subfolder
- Verify file permissions

### Category Selection Errors
- Verify category names match exactly with Marktplaats categories
- Check the double-dash separator format in Categorie.txt

### Element Not Found Errors
- Marktplaats may have updated their website structure
- Check XPATH selectors in the script
- Increase `time.sleep()` delays for slower connections

## Limitations

- Requires active Chrome browser profile
- Dependent on Marktplaats website structure (XPATHs may break with updates)
- No error recovery for failed uploads
- Single-threaded operation

## Credits

This project was originally created by [WiebAttema](https://github.com/WiebAttema/marktplaats) and was cloned from https://github.com/WiebAttema/marktplaats.

## License

Use at your own risk. Ensure compliance with Marktplaats Terms of Service regarding automated posting.

## Disclaimer

This tool is for educational and personal use. Automated posting may violate Marktplaats terms of service. Use responsibly and within their guidelines.