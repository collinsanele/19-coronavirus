from django.shortcuts import render, redirect
from django.http import JsonResponse


import requests
from bs4 import BeautifulSoup



headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
			}



#Webscraping here


#Function that takes a country name as a parameter and returns data for that country

def get_country_data(country_query):
	url = "https://www.worldometers.info/coronavirus/country/"+str(country_query)+"/"
	r = requests.get(url, headers=headers)
	soup = BeautifulSoup(r.content, "html.parser")
	total_str = soup.find("div", class_="maincounter-number").find("span").text.strip()
	total_deaths_str = soup.findAll("div", class_="maincounter-number")[1].find("span").text.strip()
	total_recovered_str = soup.findAll("div", class_="maincounter-number")[2].find("span").text.strip()
	
	total_cases = int(total_str.replace(",", "").replace(".","").strip())
	total_deaths = int(total_deaths_str.replace(",", "").replace(".","").strip())
	
	try:
		total_recovered = int(total_recovered_str.replace(",", "").replace(".","").strip())
		
	except:
		total_recovered = 0
		
	
	
	data = {"total_cases":total_cases, "deaths":total_deaths, "recovered":total_recovered, "case_type":country_query.upper(),
			"total_str":total_str, "total_deaths_str":total_deaths_str, "total_recovered_str":total_recovered_str,
			"countries_data":countries_data}
			
	return data







def get_countries():
	r = requests.get("https://www.worldometers.info/coronavirus/")
	soup = BeautifulSoup(r.content, "html.parser")

	countries_raw = soup.find("table", {"id":"main_table_countries_today"}).findAll("a", class_="mt_a")

	countries_text = [country.text.strip() for country in countries_raw]
	countries_inner_text = [country.get("href").split("country")[-1].replace("/","").strip() for country in countries_raw]
	countries_inner_text = sorted(countries_inner_text)
	
	return countries_inner_text
	

#Call countries_data so all functions can use it
countries_data = get_countries()




def get_world_data():
	r = requests.get("https://www.worldometers.info/coronavirus/?", headers=headers)
	soup = BeautifulSoup(r.content, "html.parser")
	total_str = soup.find("div", class_="maincounter-number").find("span").text.strip()
	total_deaths_str = soup.findAll("div", class_="maincounter-number")[1].find("span").text.strip()
	total_recovered_str = soup.findAll("div", class_="maincounter-number")[2].find("span").text.strip()
	
	total_cases = int(total_str.replace(",", "").replace(".","").strip())
	total_deaths = int(total_deaths_str.replace(",", "").replace(".","").strip())
	total_recovered = int(total_recovered_str.replace(",", "").replace(".","").strip())
	
	#countries_data = get_countries()
	
	data = {"total_cases":total_cases, "deaths":total_deaths, "recovered":total_recovered, "case_type":"World Cases",
			"total_str":total_str, "total_deaths_str":total_deaths_str, "total_recovered_str":total_recovered_str,
			"countries_data":countries_data}
	
	return data
		
	
	



#Global list to collect the data from get_world_data function to prevent
#re-running it in chart function
chart_container =[]

# Create your views here.

def home(request):

	if request.method == "POST":
		country_query = request.POST.get("q")
		if "Default" in country_query or "default" in country_query or "DEFAULT" in country_query:
			return redirect("home")
			
		url = "https://www.worldometers.info/coronavirus/country/"+str(country_query)+"/"
		r = requests.get(url, headers=headers)
		soup = BeautifulSoup(r.content, "html.parser")
		total_str = soup.find("div", class_="maincounter-number").find("span").text.strip()
		total_deaths_str = soup.findAll("div", class_="maincounter-number")[1].find("span").text.strip()
		total_recovered_str = soup.findAll("div", class_="maincounter-number")[2].find("span").text.strip()
		
		total_cases = int(total_str.replace(",", "").replace(".","").strip())
		total_deaths = int(total_deaths_str.replace(",", "").replace(".","").strip())
		
		try:
			total_recovered = int(total_recovered_str.replace(",", "").replace(".","").strip())
			
		except:
			total_recovered = 0
			
		
		
		data = {"total_cases":total_cases, "deaths":total_deaths, "recovered":total_recovered, "case_type":country_query.upper(),
				"total_str":total_str, "total_deaths_str":total_deaths_str, "total_recovered_str":total_recovered_str,
				"countries_data":countries_data}
				
		
		chart_container.append(data)
				
		context = {"data":data}
		
		return render(request, "corona_app/home.html", context)
		

	data = get_world_data()
	chart_container.append(data)
	
	context = {"data":data}
	
	return render(request, "corona_app/home.html", context)
	
	
	
	
def chart(request):
	data = chart_container[-1]
	return JsonResponse(data, safe=False)
	
	
	
def compare(request):
	
	if request.method=="POST":
		country1 = request.POST.get("q1")
		country2 = request.POST.get("q2")
		
		if country1 == "Select First Country" or country2 == "Select Second Country":
			return redirect("compare")
		
		country1_data = get_country_data(country_query=country1)
		country2_data = get_country_data(country_query=country2)
		
		context = {"country1":country1_data, "country2":country2_data, "countries_data":countries_data}
		
		return render(request, "corona_app/compare.html", context)
	
	context = {"countries_data":countries_data, "country1":[]}
	
	return render(request, "corona_app/compare.html", context)
























