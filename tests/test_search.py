import requests, os
from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome
import time


def get_expected_output_for_bengaluru_restaurants():
	url = "https://www.eazydiner.com/restaurants?location=bengaluru&meal_period=dinner"
	headers = {
		'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
		'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'accept-encoding' : 'gzip, deflate, br',
		'accept-language' : 'en-US,en;q=0.9'
	}
	page = requests.get(url, headers=headers)
	soup = bs(page.text, 'html.parser')
	elements = soup.find_all('span', attrs = {'class' : ['res_name', 'res_loc', 'cost_for_two', 'res_cuisine']})
	all_data = []
	data = {}
	for index, ele in enumerate(elements):
		if (index + 1) % 4 == 1:
			data['name'] = ele.text.strip()
		elif (index + 1) % 4 == 2:
			data['location'] = ele.text.strip()
		elif (index + 1) % 4 == 3:
			data['cost_for_two'] = ele.text.strip()
		else:
			data['cuisines'] = ele.text.strip()
			all_data.append(data)
			data = {}
	return all_data[:5]

def get_data_from_sample_webapp():
	url = "http://ec2-18-222-18-167.us-east-2.compute.amazonaws.com/"
	driver = Chrome(executable_path=os.path.join(os.getcwd(), './driver/chromedriver'))
	driver.get(url)

	time.sleep(5)

	city_name_input = driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div[1]/input')
	city_name_input.send_keys('bengaluru')

	submit_btn = driver.find_element_by_xpath('/html/body/div/div/div[1]/form/button')
	submit_btn.click()

	time.sleep(5)

	card_headers = driver.find_elements_by_class_name('card-header')
	card_bodies = driver.find_elements_by_class_name('card-text')

	all_data = []
	for header, body in zip(card_headers, card_bodies):
		header_text = header.get_attribute('textContent').strip()
		name, cost_for_two, cuisines = [i.strip() for i in header_text.split('||')]
		body_text = body.get_attribute('textContent').strip()
		address = body_text.split('Address:')[-1].strip()
		all_data.append({
			'name' : name,
			'cost_for_two' : cost_for_two,
			'cuisines' : cuisines,
			'location' : address
		})
	driver.close()
	return all_data[:5]

def test_bengaluru_results():
	output = get_data_from_sample_webapp()
	expected = get_expected_output_for_bengaluru_restaurants()
	assert output == expected

if __name__ == '__main__':
	try:
		test_bengaluru_results()
		print ('[SUCCESS] Bengaluru Test Passed!')
	except AssertionError:
		print ('[FAILED] Bengaluru Test Failed!')

