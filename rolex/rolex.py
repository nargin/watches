from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import json
import time
import re

def setup_driver():
	"""Configure and return a headless Chrome WebDriver"""
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_argument('--window-size=1920,1080')
	
	# Add headers to appear more like a real browser
	chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
	
	return webdriver.Chrome(options=chrome_options)

def scrape_watches():
	url = "https://www.rolex.com/watches/find-rolex?group=1"
	driver = setup_driver()
	
	try:
		print("Loading page...")
		driver.get(url)

		soup = BeautifulSoup(driver.page_source, 'html.parser')

		print("Site Title: ", soup.title.text)

		data_to_extract = soup.find("script", {"data-rh": "true"})

		# with open('to_extract.txt', 'w') as f:
		# 	f.write(data_to_extract.text)

		to_cut = data_to_extract.text.rfind("results:") + len("results:")

		parse = data_to_extract.text[to_cut:]

		# Add double quotes to property names if not already inside double quotes
		parse = re.sub(r'(".*?")', lambda m: m.group(1).replace(':', ';'), parse)
		# Replace every ":" inside double quotes with ";"
		parse = re.sub(r'(?<!")(\b\w+\b)(?=\s*:)', r'"\1"', parse)
		# Put every !0 and !1 inside double quotes
		parse = re.sub(r'!(0|1)', r'"\g<0>"', parse)
		

		to_cut = parse.rfind(",\"searchHubWatches\"")
		print(to_cut)
		parse = parse[:to_cut]

		# with open('no_json.json', 'w') as f:
		# 	f.write(parse)
		# 	print("Write inside file:", f.name)

		json_data = json.loads(parse)
		with open('watches.json', 'w') as f:
			f.write(json.dumps(json_data, indent=4))
			print("Write inside file:", f.name)

		# with open('rolex_page.html', 'w', encoding='utf-8') as f:
			# f.write(soup.prettify())
		
	except Exception as e:
		print(f"An error occurred: {str(e)}")
	
	finally:
		driver.quit()

if __name__ == "__main__":
	scrape_watches()

'''
{
	rmc:"m126234-0051",
	title:"Datejust 36",
	family:"Datejust",
	familyCode:"datejust",
	facet_case_title:"Oyster, 36 mm, acier Oystersteel et or gris",
	newmodelselection:!1,
	has360:!0,
	case_id:"50799",
	bracelet_id:"50813",
	urihash:"TrZPCztz0IJjRWYU",
	source:"rlx_catalog_index_2024_04",
	sourceName:"rlx_catalog_index_2024_04",
	alt:"Datejust 36, Oyster, 36 mm, acier Oystersteel et or gris, Cadran : Vert menthe, Rolex"
}
'''