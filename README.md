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
- ChromeDriver (compatible with your Chrome version)

## Required Python Libraries

```bash
pip install selenium pillow
```

## Project Structure

```
marktplaats-manager/
├── automation.py           # Main automation script
├── README.md              # This file
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

### 1. Configure Chrome Profile

Edit the Chrome user data directory path in `automation.py`:

**For Linux:**
```python
ChromeOptions.add_argument("user-data-dir=/home/YOUR_USERNAME/.config/google-chrome")
```

**For Windows:**
```python
ChromeOptions.add_argument("user-data-dir=C:\\Users\\YOUR_USERNAME\\AppData\\Local\\Google\\Chrome\\User Data")
```

### 2. Add Login Credentials

In `automation.py`, add your Marktplaats credentials (lines 60-71):

```python
email = 'your_email@example.com'
password = 'your_password'
```

### 3. Create Ad Folders

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

To run without opening a browser window, uncomment in `automation.py`:

```python
ChromeOptions.add_argument("--headless")
ChromeOptions.add_argument("--window-size=1920,1080")
```

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