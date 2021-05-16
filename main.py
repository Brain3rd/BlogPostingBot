from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
from config import chrome_path, coffee_site, blog_user, bot_email, bot_password, api_key
from webdriver_manager.chrome import ChromeDriverManager

CHROME_DRIVER_PATH = chrome_path
# driver = webdriver.Chrome(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(ChromeDriverManager().install())

coffee_blog_site = coffee_site

response = requests.get(coffee_blog_site)
blog_post = response.text

soup = BeautifulSoup(blog_post, 'html.parser')

# Get all blog titles
titles = soup.find_all('h2')
all_titles = [title.text for title in titles]
all_titles.pop(0)
all_titles.pop()
random_title = random.choice(all_titles)
print(random_title)

# Get image address
try:
    url = soup.find(name='img', alt=random_title).get('data-lazy-src')
except AttributeError:
    try:
        url = soup.find(name='img', alt=random_title.lower()).get('data-lazy-src')
    except AttributeError:
        # Or use default blog image
        url = 'https://teuvokinnunen.pythonanywhere.com/static/img/intro.jpg'
print(url)

# Make google map link
link = random_title.split()
maps = '+'.join(link)
text = f"https://www.google.com/maps/search/{maps}+Chiang+Mai"
print(text)


# Open blog website
driver.get(blog_user)

# Login
email = driver.find_element_by_xpath('//*[@id="email"]')
password = driver.find_element_by_xpath('//*[@id="password"]')
email.send_keys(bot_email)
password.send_keys(bot_password)
password.send_keys(Keys.ENTER)

sleep(3)

# Make new post
blog_title = driver.find_element_by_xpath('//*[@id="title"]')
blog_url = driver.find_element_by_xpath('//*[@id="img_url"]')
source_btn = driver.find_element_by_xpath('//*[@id="cke_33"]')
source_btn.click()
blog_title.send_keys(random_title)
blog_url.send_keys(url)
blog_text = driver.find_element_by_xpath('//*[@id="cke_1_contents"]/textarea')
blog_text.send_keys(f'Welcome to our coffee shop.<br> We are located in Chiang Mai, Thailand.'
                    f'<br>'
                    f'<iframe align="center" '
                    f'width="280" '
                    f'height="200" '
                    f'frameborder="0" style="border:0" '
                    f'src="https://www.google.com/maps/embed/v1/place?key={api_key}&q={maps},Chiang+Mai" '
                    f'allowfullscreen>'
                    f'</iframe>'
                    )
submit_btn = driver.find_element_by_xpath('//*[@id="submit"]')
submit_btn.click()

# Close browser window
driver.quit()
