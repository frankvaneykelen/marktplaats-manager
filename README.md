# Marktplaats Manager

A Python automation tool for managing Marktplaats accounts with large numbers of ads (300+). This tool automatically checks for expired ads and reposts them using Selenium web automation.

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
│   └── fotos/             # Product images
└── advertenties/          # Folder for your ads (create this)
    └── [Your Ad Name]/
        ├── Beschrijving.txt
        ├── Categorie.txt
        └── fotos/
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
3
Create a folder structure for each ad in the `advertenties/` directory:

```
advertenties/
└── My Product Name/
    ├── Beschrijving.txt
    ├── Categorie.txt
    └── fotos/
        ├── photo1.jpg
        ├── photo2.jpg
        └── photo3.jpg
```

## Ad Configuration

### Beschrijving.txt (Description)

Contains the full ad description text. Example:

```
HP Z600 Workstation (WD059AV) hexa core

Asking price: 400 euros

Works with Hackintosh, Linux and Windows.

Specifications:
- 2x Intel Xeon X5670 @ 2.93GHz (24 cores total)
- 96GB DDR3 ECC RAM
- ...

Pickup or shipping available.
```

### Categorie.txt (Category)

Format (double-dash separated):
```
Category1--Category2--Category3--Condition--PriceType--Price--ShippingOption--
```

Example:
```
Computers en Software--Computeronderdelen--Computerbehuizingen--Gebruikt--Vraagprijs--400,00--Zwaar--
```

**Field Descriptions:**

| Field | Description | Example Values |
|-------|-------------|----------------|
| Category1 | Main category | Computers en Software |
| Category2 | Subcategory | Computeronderdelen |
| Category3 | Sub-subcategory | Computerbehuizingen |
| Condition | Item condition | Nieuw, Gebruikt |
| PriceType | Pricing method | Vraagprijs, Bieden |
| Price | Price amount | 400,00 |
| ShippingOption | Shipping size | Klein, Licht, Groot, Zwaar |

**Shipping Options:**

- **Klein** (Small): Fits in mailbox, 100-350g
- **Licht** (Light): Fits in mailbox, 0-2kg
- **Groot** (Large): Doesn't fit in mailbox, 0-10kg
- **Zwaar** (Heavy): Doesn't fit in mailbox, 10-23kg

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
- Ensure photos are in the `fotos/` subfolder
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