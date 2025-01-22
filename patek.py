from driver import setup_driver
from bs4 import BeautifulSoup
import json, re

def main():
	url = "https://www.patek.com/en/collection/all-models"
	driver = setup_driver()
	
	try:
		print("Loading page...")
		driver.get(url)

		soup = BeautifulSoup(driver.page_source, 'html.parser')

		print(soup.prettify())
	
	except Exception as e:
		print(f"An error occurred: {str(e)}")
	
if __name__ == "__main__":
	main()