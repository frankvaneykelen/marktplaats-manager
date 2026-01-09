from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException   
import os
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ExifTags
import json

# Import configuration
try:
    from config import EMAIL as email, PASSWORD as password, CHROME_USER_DATA_DIR, HEADLESS_MODE, WINDOW_SIZE
except ImportError:
    print("Error: config.py not found!")
    print("Please copy config.example.py to config.py and fill in your settings.")
    exit(1)

# Load category data
def load_categories():
    """Load category hierarchy from scraped JSON files"""
    try:
        with open('categories/parents.json', encoding='utf-8') as f:
            parents = json.load(f)
        with open('categories/children.json', encoding='utf-8') as f:
            children = json.load(f)
        with open('categories/grandchildren.json', encoding='utf-8') as f:
            grandchildren = json.load(f)
        return parents, children, grandchildren
    except Exception as e:
        print(f"Warning: Could not load category data: {e}")
        print("Run 'python scrape_categories.py' first to generate category files.")
        return None, None, None

def find_category_ids(parent_name, child_name, grandchild_name):
    """Find category IDs from names using scraped data"""
    parents, children, grandchildren = load_categories()
    
    if not all([parents, children, grandchildren]):
        return None, None, None
    
    # Find parent ID
    parent = next((p for p in parents if p['name'] == parent_name), None)
    if not parent:
        print(f"Warning: Parent category '{parent_name}' not found")
        return None, None, None
    parent_id = parent['id']
    
    # Find child ID
    child = next((c for c in children if c['name'] == child_name and c['parentId'] == parent_id), None)
    if not child:
        print(f"Warning: Child category '{child_name}' not found under '{parent_name}'")
        return parent_id, None, None
    child_id = child['id']
    
    # Find grandchild ID
    grandchild = next((g for g in grandchildren if g['name'] == grandchild_name and g['parentId'] == child_id), None)
    if not grandchild:
        print(f"Warning: Grandchild category '{grandchild_name}' not found under '{child_name}'")
        return parent_id, child_id, None
    grandchild_id = grandchild['id']
    
    return parent_id, child_id, grandchild_id

# Setup Chrome WebDriver
ChromeOptions = webdriver.ChromeOptions()
ChromeOptions.add_argument(f"user-data-dir={CHROME_USER_DATA_DIR}")
ChromeOptions.add_argument("--profile-directory=Default")  # Use default profile
ChromeOptions.add_argument("disable-blink-features=AutomationControlled")
ChromeOptions.add_argument("--ignore-certificate-errors")
ChromeOptions.add_argument('--allow-running-insecure-content')
ChromeOptions.add_argument("--no-sandbox")  # Bypass OS security model
ChromeOptions.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
ChromeOptions.add_argument("--remote-debugging-port=9222")  # Enable DevTools
if HEADLESS_MODE:
    ChromeOptions.add_argument("--headless")
    ChromeOptions.add_argument(f"--window-size={WINDOW_SIZE}")
WebDriver = webdriver.Chrome(options = ChromeOptions)
time.sleep(2)

def check_exists_by_xpath(xpath):
    try:
        WebDriver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

WebDriver.maximize_window()
time.sleep(2)

WebDriver.get('https://www.marktplaats.nl')
time.sleep(3)

# Handle cookie consent - it's inside an iframe
try:
    wait = WebDriverWait(WebDriver, 10)
    # Wait for the iframe to appear
    iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title*='Consent']")))
    WebDriver.switch_to.frame(iframe)
    
    # Now click the accept button inside the iframe
    accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accepteren') or contains(text(), 'Accept')]")))
    accept_button.click()
    
    # Switch back to main content
    WebDriver.switch_to.default_content()
    time.sleep(3)
except Exception:
    # Cookie consent already accepted or not present
    WebDriver.switch_to.default_content()

# Wait for any overlays to disappear
time.sleep(3)

inloggen_popup = '/html/body/div[4]/div/div/div[1]/div[1]/button'
if check_exists_by_xpath(inloggen_popup) != False:
    inloggen_popup = WebDriver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[1]/div[1]/button')
    inloggen_popup.click()
    time.sleep(5)

naam_zwm = '//*[@id="header-root"]/header/div[1]/div[2]/div/ul[2]/li[3]/div/button/span'
naam_mwm = '//*[@id="header-root"]/header/div[1]/div[2]/div/ul[2]/li[4]/div/button/span'

if check_exists_by_xpath(naam_zwm) != True and check_exists_by_xpath(naam_mwm) != True:
    try:
        # Use JavaScript click to avoid interception
        inloggen_header = WebDriver.find_element(By.XPATH, '//*[@id="header-root"]/header/div[1]/div[2]/div/ul[2]/li[4]/a')
        WebDriver.execute_script("arguments[0].click();", inloggen_header)
        time.sleep(5)
    except Exception:
        pass
        time.sleep(2)

    # Wait for login form to appear
    try:
        wait = WebDriverWait(WebDriver, 10)
        form_email = wait.until(EC.presence_of_element_located((By.ID, 'email')))
        
        form_email.clear()
        form_email.send_keys(email)
        time.sleep(2)

        form_password = WebDriver.find_element(By.ID, 'password')
        form_password.clear()
        form_password.send_keys(password)
        time.sleep(2)    

        # Find and click the login button
        try:
            inloggen_submit = WebDriver.find_element(By.XPATH, "//button[contains(text(), 'Inloggen met je e-mailadres')]")
            inloggen_submit.click()
            time.sleep(5)
        except:
            # Alternative: press Enter on password field
            form_password.send_keys('\n')
            time.sleep(5)
        
    except Exception:
        # Already logged in
        pass

# Wait for login to complete and page to load
time.sleep(3)

if check_exists_by_xpath('//*[@id="header-root"]/header/div[1]/div[2]/div/ul[2]/li[3]/div/button') != False:
    naam_dropdown = WebDriver.find_element(By.XPATH, '//*[@id="header-root"]/header/div[1]/div[2]/div/ul[2]/li[3]/div/button')
    naam_dropdown.click()
    time.sleep(1)
    mijn_advertenties = WebDriver.find_element(By.XPATH, '//*[@id="header-root"]/header/div[1]/div[2]/div/ul[2]/li[3]/div/ul/li[1]/a')
    mijn_advertenties.click()
    time.sleep(2)
elif check_exists_by_xpath('//*[@id="header-root"]/header/div[1]/div[2]/div/ul[2]/li[4]/div/button') != False:
    naam_dropdown = WebDriver.find_element(By.XPATH, '//*[@id="header-root"]/header/div[1]/div[2]/div/ul[2]/li[4]/div/button')
    naam_dropdown.click()
    time.sleep(1)
    mijn_advertenties = WebDriver.find_element(By.XPATH, '//*[@id="header-root"]/header/div[1]/div[2]/div/ul[2]/li[4]/div/ul/li[1]/a')
    mijn_advertenties.click()
    time.sleep(2)
else:
    print("ERROR: Not logged in")
    WebDriver.close()
    exit(1)

meer_advertenties = '//*[@id="load-more-row"]/div/a'

while check_exists_by_xpath(meer_advertenties) != False:

    toon_meer_advertenties = WebDriver.find_element(By.XPATH, '//*[@id="load-more-row"]/div/a')
    toon_meer_advertenties.click()
    time.sleep(3)

my_list = [d for d in os.listdir('ads') if os.path.isdir(os.path.join('ads', d)) and d != '.tmp.driveupload']
print(f"Found {len(my_list)} ad folders locally")

# Get existing ads from Marktplaats using flexible selector
advertentie_naam_div = WebDriver.find_elements(By.XPATH, '//*[contains(@class, "ad-listing")]//div[@class="description-title"]')

advertentie_online_list = []

for i in advertentie_naam_div:
    try:
        advertenties_op_marktplaats = i.find_element(By.TAG_NAME, 'span').text
        advertentie_online_list.append(advertenties_op_marktplaats)
    except:
        continue

print(f"Found {len(advertentie_online_list)} ads online, {len(my_list)} ads locally")

ads_niet_op_marktplaats = [i for i in my_list if i not in advertentie_online_list]

if ads_niet_op_marktplaats:
    print(f"Posting {len(ads_niet_op_marktplaats)} new ads: {', '.join(ads_niet_op_marktplaats)}")
else:
    print("All ads already online")


for i in ads_niet_op_marktplaats:
    print(f"\nProcessing: {i}")

    # Navigate to homepage first, then click "Plaats advertentie"
    try:
        WebDriver.get('https://www.marktplaats.nl')
        time.sleep(5)
        
        # Try to find and click the "Plaats advertentie" button
        if check_exists_by_xpath('//*[@id="header-root"]/header/div[1]/div[2]/div/ul[2]/li[6]/a') != False:
            plaats_advertentie = WebDriver.find_element(By.XPATH, '//*[@id="header-root"]/header/div[1]/div[2]/div/ul[2]/li[6]/a')
            plaats_advertentie.click()
            time.sleep(3)
        elif check_exists_by_xpath('//*[@id="header-root"]/header/div[1]/div[2]/div/ul[2]/li[5]/a') != False:
            plaats_advertentie = WebDriver.find_element(By.XPATH, '//*[@id="header-root"]/header/div[1]/div[2]/div/ul[2]/li[5]/a')
            plaats_advertentie.click()
            time.sleep(3)
        else:
            # Fallback: navigate directly
            WebDriver.get('https://www.marktplaats.nl/plaatsen/')
            time.sleep(5)
    except Exception as e:
        print(f"Navigation error: {e}")
        continue

    # Wait for the ad creation page to load
    wait = WebDriverWait(WebDriver, 15)
    input_advertentienaam = wait.until(EC.presence_of_element_located((By.ID, 'TextField-vulEenTitelIn')))
    input_advertentienaam.send_keys(i)
    time.sleep(2)

    # Read index.txt and split category line from description
    with open(f'ads/{i}/index.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('\n---\n', 1)
    category_line = parts[0].strip()
    beschrijving_text = parts[1].strip() if len(parts) > 1 else ""
    
    # Parse category fields
    file_contents = category_line.split("--")
    
    # Look up category IDs from scraped data
    parent_id, child_id, grandchild_id = find_category_ids(file_contents[0], file_contents[1], file_contents[2])
    
    if parent_id:
        eerste_select = Select(WebDriver.find_element(By.ID, 'cat_sel_1'))
        eerste_select.select_by_value(str(parent_id))
        print(f"Category 1 selected: {file_contents[0]} (ID: {parent_id})")
        time.sleep(2)
    else:
        print(f"ERROR: Could not find parent category '{file_contents[0]}'")
        continue

    if child_id:
        tweede_select = Select(WebDriver.find_element(By.ID, 'cat_sel_2'))
        tweede_select.select_by_value(str(child_id))
        print(f"Category 2 selected: {file_contents[1]} (ID: {child_id})")
        time.sleep(2)
    else:
        print(f"ERROR: Could not find child category '{file_contents[1]}'")
        continue

    if grandchild_id:
        derde_select = Select(WebDriver.find_element(By.ID, 'cat_sel_3'))
        derde_select.select_by_value(str(grandchild_id))
        print(f"Category 3 selected: {file_contents[2]} (ID: {grandchild_id})")
        time.sleep(2)
    else:
        print(f"ERROR: Could not find grandchild category '{file_contents[2]}'")
        continue

    # Find and click submit button
    try:
        wait = WebDriverWait(WebDriver, 10)
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="redirectToPlaceAd"]')))
        submit_button.click()
        time.sleep(5)
    except Exception as e:
        print(f"ERROR: Could not find submit button: {e}")
        continue

    # Description already loaded from index.txt
    photos_folder = f'ads/{i}/photos'
    my_photos = os.listdir(photos_folder)
    upload_vak = 0

    for i in my_photos:
        path = f'{photos_folder}/{i}'
        newphoto = i
        # Check if image needs rotation (skip PNG files)
        if not path.lower().endswith('.png'):
            try:

                image = Image.open(path)

                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation]=='Orientation':
                        break
                    
                exif = image._getexif()
                print(exif[orientation])
                image.close()
                image = Image.open(path).convert('RGBA')

                if exif[orientation] == 3:
                    image=image.rotate(180, expand=True)
                    image.save(path  + ".PNG", "PNG")
                    os.remove(path)
                    newphoto = i + ".PNG"
                elif exif[orientation] == 6:
                    image=image.rotate(270, expand=True)
                    image.save(path  + ".PNG", "PNG")
                    os.remove(path)
                    newphoto = i + ".PNG"
                elif exif[orientation] == 8:
                    image=image.rotate(90, expand=True)
                    image.save(path  + ".PNG", "PNG")
                    os.remove(path)
                    newphoto = i + ".PNG"
                        
            except (AttributeError, KeyError, IndexError, TypeError):
                # cases: image don't have getexif
                pass

        # Upload photo using the file input
        try:
            wait = WebDriverWait(WebDriver, 10)
            file_input = wait.until(EC.presence_of_element_located((By.ID, 'imageUploader-hiddenInput')))
            path = f'{os.getcwd()}/{photos_folder}/{newphoto}'
            file_input.send_keys(path)
            print(f"Photo uploaded: {newphoto}")
            time.sleep(2)  # Wait for upload to process
        except Exception as e:
            print(f"ERROR: Could not upload photo {newphoto}: {e}")
            continue
    
    time.sleep(2)

    # Fill in description using new rich text editor (from index.txt)
    try:
        wait = WebDriverWait(WebDriver, 10)
        description_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="text-editor-input_nl-NL"]')))
        description_field.send_keys(beschrijving_text)
        time.sleep(2)
    except Exception as e:
        print(f"ERROR: Could not fill description: {e}")
        continue

    # Format: Parent--Child--Grandchild--Subject--Year--Condition--PriceType--Price--PackageSize
    # Example: Boeken--Kunst en Cultuur--Beeldend--Beeldhouwkunst--1997--Gelezen--Bieden----Klein pakket
    
    # Subject (if exists - field 3 for books)
    if len(file_contents) > 3 and file_contents[3]:
        try:
            subject_select = Select(WebDriver.find_element(By.ID, 'singleSelectAttribute[subject]'))
            subject_select.select_by_visible_text(file_contents[3])
            print(f"Subject selected: {file_contents[3]}")
            time.sleep(1)
        except:
            print(f"Subject field not found or couldn't select '{file_contents[3]}'")
    
    # Year (if exists - field 4)
    if len(file_contents) > 4 and file_contents[4]:
        try:
            year_input = WebDriver.find_element(By.ID, 'numericAttribute[yearOriginal]')
            year_input.send_keys(file_contents[4])
            time.sleep(1)
        except:
            pass
    
    # Condition (if exists - field 5)
    if len(file_contents) > 5 and file_contents[5]:
        try:
            condition_select = Select(WebDriver.find_element(By.ID, 'singleSelectAttribute[condition]'))
            condition_select.select_by_visible_text(file_contents[5])
            time.sleep(1)
        except:
            pass

    # Price type (field 6)
    if len(file_contents) > 6 and file_contents[6]:
        try:
            price_type_select = Select(WebDriver.find_element(By.ID, 'Dropdown-prijstype'))
            price_type_select.select_by_visible_text(file_contents[6])
            time.sleep(1)
        except:
            pass

    # Delivery method - Ophalen of Verzenden should already be selected
    # Carriers - Leave as default (PostNL and DHL checked)
    time.sleep(1)

    # Package size (if specified - field 8)
    if len(file_contents) > 8 and file_contents[8]:
        package_size_map = {
            'Brievenbuspakje': 'Radio-brievenbuspakje-xs',
            'Klein pakket': 'Radio-kleinPakket-s',
            'Gemiddeld pakket': 'Radio-gemiddeldPakket-m',
            'Groot pakket': 'Radio-grootPakket-l'
        }
        if file_contents[8] in package_size_map:
            try:
                package_radio = WebDriver.find_element(By.ID, package_size_map[file_contents[8]])
                package_radio.click()
                print(f"Package size selected: {file_contents[8]}")
                time.sleep(1)
            except:
                print(f"Could not select package size '{file_contents[8]}'")

    # Deselect phone number display
    try:
        phone_switch = WebDriver.find_element(By.ID, 'syi-phonenumber-switch-input')
        if phone_switch.is_selected():
            phone_switch.click()
            print("Phone number display disabled")
        time.sleep(1)
    except:
        print("Could not find phone number switch")

    # Select "Gratis" ad type
    try:
        wait = WebDriverWait(WebDriver, 10)
        gratis_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="bundle-option-FREE"]')))
        gratis_button.click()
        print("Gratis ad type selected")
        time.sleep(2)
    except Exception as e:
        print(f"Could not select Gratis ad type: {e}")

    # Submit the ad
    try:
        wait = WebDriverWait(WebDriver, 10)
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="place-listing-submit-button"]')))
        submit_button.click()
        print(f"✓ {i}")
        time.sleep(5)
    except Exception as e:
        print(f"ERROR: Could not submit ad: {e}")
        continue

# Close browser
time.sleep(5)
WebDriver.close()
print("\nDone!")

