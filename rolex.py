from bs4 import BeautifulSoup
import json
import time
import re
from driver import setup_driver

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

		not_parsed = parse[to_cut:]
		parse = parse[:to_cut]
		# print(not_parsed)

		json_data = json.loads(parse)
		with open('rolex/watches.json', 'w') as f:
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