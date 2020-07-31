from flask import Flask, render_template, request, redirect, url_for
import subprocess
from datetime import datetime

def execute_curl_command_and_get_page_source(cmd):
	p = subprocess.check_output(['/bin/bash', '-c', cmd])
	return p

def get_top_5_data():
	names_cmd = "cat ./tmp/temp.html | grep \'res_name\">\' | sed \'s/^.*res_name\">//\' | sed \'s/<\\/span>//\'"
	names = subprocess.check_output(['/bin/bash', '-c', names_cmd]).decode('utf-8').split('\n')

	address_cmd = "cat ./tmp/temp.html | grep \'res_loc\' | sed \'s/^.*res_loc.*\">//\' | sed \'s/<\\/span>//\'"
	addresses = [a for a in subprocess.check_output(['/bin/bash', '-c', address_cmd]).decode('utf-8').split('\n') if '\\n' not in a]

	costs_for_two_cmd = "cat ./tmp/temp.html | grep \'cost_for_two\' | sed \'s/^.*cost_for_two.*\">//\' | sed \'s/<\\/span>//\' | sed \'s/<\\/span>//\'"
	costs_for_two = [a for a in subprocess.check_output(['/bin/bash', '-c', costs_for_two_cmd]).decode('utf-8').split('\n') if '\\n' not in a]

	cuisines_cms = "cat ./tmp/temp.html | grep \'res_cuisine\' | sed \'s/^.*res_cuisine.*\" >//\' | sed \'s/<\\/span>//\'"
	cuisines = subprocess.check_output(['/bin/bash', '-c', cuisines_cms]).decode('utf-8').split('\n')

	all_data = []
	count = 0
	for name, address, cost4two, cuisine in zip(names, addresses, costs_for_two, cuisines):
		if name and address and cost4two:
			all_data.append({
				"name" : name,
				"address" : address,
				"cost_for_two" : cost4two,
				"cuisine" : cuisine
			})
			count += 1
			if count >= 5:
				break

	return all_data

def form_curl_command(city, cuisines=None, cost_for_two=None):
	cmd = "curl -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' -H 'referer: https://www.zomato.com/' 'https://www.eazydiner.com/restaurants?location={}&date={}".format(city.lower(), datetime.now().__str__().split(' ')[0])
	if cuisines and cuisines != []:
		for cuisine in cuisines:
			cmd += "&cuisines%5B%5D={}".format(cuisine.lower().replace(' ', '-'))
	cmd += "&meal_period=dinner'"
	return cmd

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
	return render_template('home.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
	if request.method == 'POST':
	    form_data = request.form
	    city = form_data.get('city')
	    cuisines = [c for c in form_data.get('cuisine').split(',') if c.strip() != '']

	    curl_cmd = form_curl_command(city=city, cuisines=cuisines)

	    page = execute_curl_command_and_get_page_source(curl_cmd)

	    with open('./tmp/temp.html', 'wb') as f:
	    	f.write(page)

	    data = get_top_5_data()

	    return render_template('home.html', data=data)


if __name__ == '__main__':
   app.run()
