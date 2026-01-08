from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException   
import os
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ExifTags

# Import configuration
try:
    from config import EMAIL as email, PASSWORD as password, CHROME_USER_DATA_DIR, HEADLESS_MODE, WINDOW_SIZE
except ImportError:
    print("Error: config.py not found!")
    print("Please copy config.example.py to config.py and fill in your settings.")
    exit(1)

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
    print("Switched to consent iframe")
    
    # Now click the accept button inside the iframe
    accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accepteren') or contains(text(), 'Accept')]")))
    accept_button.click()
    print("Cookie consent accepted")
    
    # Switch back to main content
    WebDriver.switch_to.default_content()
    time.sleep(3)
except Exception as e:
    print(f"No cookie consent found or already accepted: {e}")
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
        print("Login button clicked")
        time.sleep(5)
    except Exception as e:
        print(f"Could not click login button: {e}")
        time.sleep(2)

    # Wait for login form to appear
    try:
        wait = WebDriverWait(WebDriver, 10)
        form_email = wait.until(EC.presence_of_element_located((By.ID, 'email')))
        
        form_email.clear()
        form_email.send_keys(email)
        print("Email entered")
        time.sleep(2)

        form_password = WebDriver.find_element(By.ID, 'password')
        form_password.clear()
        form_password.send_keys(password)
        print("Password entered")
        time.sleep(2)    

        # Find and click the login button
        try:
            inloggen_submit = WebDriver.find_element(By.XPATH, "//button[contains(text(), 'Inloggen met je e-mailadres')]")
            inloggen_submit.click()
            print("Login submitted")
            time.sleep(5)
        except:
            # Alternative: press Enter on password field
            form_password.send_keys('\n')
            print("Login submitted via Enter key")
            time.sleep(5)
        
    except Exception as e:
        print(f"Login form not found or already logged in: {e}")

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
    print("Could not find account dropdown - might not be logged in")
    WebDriver.close()
    exit(1)

meer_advertenties = '//*[@id="load-more-row"]/div/a'

while check_exists_by_xpath(meer_advertenties) != False:

    toon_meer_advertenties = WebDriver.find_element(By.XPATH, '//*[@id="load-more-row"]/div/a')
    toon_meer_advertenties.click()
    time.sleep(3)

my_list = os.listdir('advertenties')

advertentie_naam_div = WebDriver.find_elements(By.XPATH, '//*[@class="row ad-listing"]/div/div[3]/div[1]')
print(len(advertentie_naam_div))

advertentie_online_list = []

for i in advertentie_naam_div:

    advertenties_op_marktplaats = i.find_element(By.TAG_NAME, 'span').text
    advertentie_online_list.append(advertenties_op_marktplaats)

print(len(advertentie_online_list))

advertenties_niet_op_marktplaats = []

for i in my_list:

    if i not in advertentie_online_list:

        advertenties_niet_op_marktplaats.append(i)
        print(i)
        
print(len(advertenties_niet_op_marktplaats))


for i in advertenties_niet_op_marktplaats:

    homepage = WebDriver.find_element(By.XPATH, '/html/body/mp-header/div[1]/div[2]/div/a')
    homepage.click()
    time.sleep(10)

    if check_exists_by_xpath('//*[@id="header-root"]/header/div[1]/div[2]/div/ul[2]/li[6]/a') != False:
        plaats_advertentie = WebDriver.find_element(By.XPATH, '//*[@id="header-root"]/header/div[1]/div[2]/div/ul[2]/li[6]/a')
        plaats_advertentie.click()
        time.sleep(3)

    elif check_exists_by_xpath('//*[@id="header-root"]/header/div[1]/div[2]/div/ul[2]/li[5]/a') != False:
        plaats_advertentie = WebDriver.find_element(By.XPATH, '//*[@id="header-root"]/header/div[1]/div[2]/div/ul[2]/li[5]/a')
        plaats_advertentie.click()
        time.sleep(3)

    # Wait for the ad creation page to load
    wait = WebDriverWait(WebDriver, 10)
    input_advertentienaam = wait.until(EC.presence_of_element_located((By.ID, 'TextField-vulEenTitelIn')))
    input_advertentienaam.send_keys(i)
    print(f"Ad title entered: {i}")
    time.sleep(2)

    f = open(f'advertenties/{i}/Categorie.txt', 'r')
    file_contents = f.read()
    file_contents = file_contents.split("--")

    eerste_select = Select(WebDriver.find_element(By.ID, 'cat_sel_1'))
    eerste_select.select_by_visible_text(file_contents[0])
    print(f"Category 1 selected: {file_contents[0]}")
    time.sleep(2)

    tweede_select = Select(WebDriver.find_element(By.ID, 'cat_sel_2'))
    tweede_select.select_by_visible_text(file_contents[1])
    print(f"Category 2 selected: {file_contents[1]}")
    time.sleep(2)

    derde_select = Select(WebDriver.find_element(By.ID, 'cat_sel_3'))
    derde_select.select_by_visible_text(file_contents[2])
    print(f"Category 3 selected: {file_contents[2]}")
    time.sleep(2)

    submit_advertentienaam = WebDriver.find_element(By.XPATH, '//*[@id="category-selection-submit"]')
    submit_advertentienaam.click()
    time.sleep(5)

    beschrijving_path = f'advertenties/{i}/Beschrijving.txt' 
    photos_folder = f'advertenties/{i}/fotos'
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

        while True:
            foto_upload_div = WebDriver.find_elements(By.XPATH, '//*[@class="moxie-shim moxie-shim-html5"]')
            try:
                foto_upload = foto_upload_div[upload_vak].find_element(By.TAG_NAME, 'input')
            except IndexError:
                time.sleep(1)
                continue
            else:
       		       
                path = f'{os.getcwd()}/{photos_folder}/{newphoto}'
                foto_upload.send_keys(path)
                upload_vak+=1
                break
    time.sleep(1)

    beschrijving = open(beschrijving_path, 'r')
    beschrijving_text = beschrijving.read()
    textvak_beschrijving_frame = WebDriver.find_element(By.XPATH, '//*[@id="description_nl-NL_ifr"]')
    WebDriver.switch_to.frame(textvak_beschrijving_frame)
    textvak_beschrijving = WebDriver.find_element(By.XPATH, "//body")
    textvak_beschrijving.send_keys(beschrijving_text)
    time.sleep(2)

    WebDriver.switch_to.default_content()
    if check_exists_by_xpath('//*[@id="syi-attribute-condition"]/div/select') != False:
        conditie_select = Select(WebDriver.find_element(By.XPATH, '//*[@id="syi-attribute-condition"]/div/select'))
        conditie_select.select_by_visible_text(file_contents[3])
        time.sleep(2)

    prijstype_select = Select(WebDriver.find_element(By.XPATH, '//*[@id="syi-price-type-dropdown"]/div/select'))
    prijstype_select.select_by_visible_text(file_contents[4])
    time.sleep(2)

    if file_contents[4] == 'Vraagprijs':
        vraagprijs = WebDriver.find_element(By.XPATH, '//*[@id="syi-bidding-price"]/input')
        vraagprijs.send_keys(file_contents[5])
        time.sleep(3)

        bieden = WebDriver.find_element(By.XPATH, '//*[@id="syi-bidding-accept"]/span/label')
        biedprijs = WebDriver.find_element(By.XPATH, '//*[@id="syi-price-type"]/div[1]/div[2]/div[2]')
        biedprijs_stijl = biedprijs.get_attribute("style")
        print(biedprijs_stijl)
        if biedprijs_stijl == 'display: none;':
            bieden.click()
        time.sleep(1)

    verzendmethode = WebDriver.find_element(By.XPATH, '//*[@id="shippingMethod0"]')
    verzendmethode.click()
    time.sleep(2)

    if file_contents[5] == 'Klein' or file_contents[6] == 'Klein':
        past_door_bus = WebDriver.find_element(By.XPATH, '//*[@id="PostNLShippingProducts"]/div[1]/div[2]/div/div/div[2]/label[1]/input')
        past_door_bus.click()
        time.sleep(2)

        envelop = WebDriver.find_element(By.XPATH, '//*[@id="1000_letters_175"]')
        envelop.click()
        time.sleep(2)

        verzendmethode_opslaan = WebDriver.find_element(By.XPATH, '//*[@id="PostNLShippingProducts"]/div[1]/div[3]/button[2]')
        verzendmethode_opslaan.click()

    elif file_contents[5] == 'Licht' or file_contents[6] == 'Licht':
        past_door_bus = WebDriver.find_element(By.XPATH, '//*[@id="PostNLShippingProducts"]/div[1]/div[2]/div/div/div[2]/label[1]/input')
        past_door_bus.click()
        time.sleep(2)

        brievenbuspakje = WebDriver.find_element(By.XPATH, '//*[@id="1018_parcels_1000"]')
        brievenbuspakje.click()
        time.sleep(2)

        verzendmethode_opslaan = WebDriver.find_element(By.XPATH, '//*[@id="PostNLShippingProducts"]/div[1]/div[3]/button[2]')
        verzendmethode_opslaan.click()

    elif file_contents[5] == 'Groot' or file_contents[6] == 'Groot':
        past_niet_door_bus = WebDriver.find_element(By.XPATH, '//*[@id="PostNLShippingProducts"]/div[1]/div[2]/div/div/div[2]/label[2]/input')
        past_niet_door_bus.click()
        time.sleep(2)

        pakket_0_tot_10_kg = WebDriver.find_element(By.XPATH, '//*[@id="3000_parcels_5000"]')
        pakket_0_tot_10_kg.click()
        time.sleep(2)

        verzendmethode_opslaan = WebDriver.find_element(By.XPATH, '//*[@id="PostNLShippingProducts"]/div[1]/div[3]/button[2]')
        verzendmethode_opslaan.click()

    elif file_contents[5] == 'Zwaar' or file_contents[6] == 'Zwaar':
        past_niet_door_bus = WebDriver.find_element(By.XPATH, '//*[@id="PostNLShippingProducts"]/div[1]/div[2]/div/div/div[2]/label[2]/input')
        past_niet_door_bus.click()
        time.sleep(2)

        pakket_10_tot_23_kg = WebDriver.find_element(By.XPATH, '//*[@id="3001_parcels_16500"]')
        pakket_10_tot_23_kg.click()
        time.sleep(2)

        verzendmethode_opslaan = WebDriver.find_element(By.XPATH, '//*[@id="PostNLShippingProducts"]/div[1]/div[3]/button[2]')
        verzendmethode_opslaan.click()

    time.sleep(2)

    kopersbescherming = WebDriver.find_element(By.XPATH, '//*[@id="syi-buyer-protection"]/div[2]/label')
    kopersbescherming.click()
    time.sleep(2)

    gratis = WebDriver.find_element(By.XPATH, '//*[@id="js-products"]/div[1]/div/div/div[1]/div[1]/span')
    gratis.click()
    time.sleep(2)

    plaatsen = WebDriver.find_element(By.XPATH, '//*[@id="syi-place-ad-button"]')
    plaatsen.click()
    time.sleep(5)
  
    feedback = '//*[@id="survey-web-page-wrapper"]/div/div[4]/button[1]'

    if check_exists_by_xpath(feedback) != False:
        feedback_sluit = WebDriver.find_element(By.XPATH, feedback)
        feedback_sluit.click()
        time.sleep(2)

time.sleep(20)
WebDriver.close()
