#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/12/15'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
             ┏┓   ┏┓
            ┏┛┻━━━┛┻┓
            ┃       ┃
            ┃ ┳┛ ┗┳ ┃
            ┃   ┻   ┃
            ┗━┓   ┏━┛
              ┃   ┗━━━┓
              ┃神兽保佑┣┓
              ┃永无BUG  ┏┛
              ┗┓┓┏━┳┓┏━┛
               ┃┫┫ ┃┫┫
               ┗┻┛ ┗┻┛
"""
import requests
from bs4 import BeautifulSoup
import os
import json
import random
from flask import *

app = Flask(__name__)

ZHI = ['北京', '上海', '澳门', '香港', '重庆', '天津']

citys_dict = {}


def get_city_list():
    global citys_dict
    base_url = "http://qq.ip138.com"
    weather_url = base_url + "/weather"
    response = requests.get(weather_url)
    response_text = response.text.encode("iso-8859-1").decode('gbk')
    urls_text = BeautifulSoup(response_text, features="html.parser").find("tr", attrs={'class': 'bg5'})
    urls_text = urls_text.find_all("td")
    for url_text in urls_text[:-1]:
        if url_text:
            citys_name = url_text.find("a").get_text()
            city_url = base_url + url_text.find("a").get("href")
            if citys_name in ZHI:
                citys_dict[citys_name] = {
                    'city_name': citys_name,
                    'city_url': city_url
                }
                print("get " + citys_name + " data...")
            else:
                response = requests.get(city_url)
                response_text = response.text.encode("iso-8859-1").decode('gbk')
                citys = BeautifulSoup(response_text, features="html.parser").find("div", id="CityList").find_all(
                    "td")
                for city in citys:
                    if city.find("a") and city.find("a").has_attr("href"):
                        city_name = city.find("a").get_text()
                        city_url = base_url + city.find("a").get("href")
                        citys_dict[city_name] = {
                            'city_name': city_name,
                            'city_url': city_url
                        }
                        print("get " + citys_name + " " + city_name + " data...")


def get_weather(city_data):
    city_url = city_data['city_url']
    response = requests.get(city_url)
    response_text = response.text.encode("iso-8859-1").decode('gbk')
    response_text = BeautifulSoup(response_text, features="html.parser")
    date_list_text = response_text.find("tr", attrs={'class': 'bg5'})
    date_list = [date.get_text() for date in date_list_text.find_all("td")]
    other_data_list = date_list_text.find_next_siblings("tr")
    weather_list = [data.get_text() for data in other_data_list[0].find_all("td")]
    tem_list = [data.get_text() for data in other_data_list[1].find_all("td")]
    wind_list = [data.get_text() for data in other_data_list[2].find_all("td")]
    
    res = [{'date': date.split(" ")[1], 'weather': weather, 'wind': wind, 'tem': tem} for date, weather, wind, tem in
           zip(date_list, weather_list, wind_list, tem_list)]
    return res


def get_random_citys():
    global citys_dict
    return random.sample(citys_dict.keys(), 5)


@app.route('/')
def index():
    global citys_dict
    city_list = get_random_citys()
    weather_list = [get_weather(citys_dict[city]) for city in city_list]
    print(weather_list)
    return render_template("index.html", city_list=city_list, weather_list=weather_list)


@app.route('/search/<name>')
def search(name):
    global citys_dict
    if name in citys_dict.keys():
        weather_data = get_weather(citys_dict[name])
        return render_template("search.html",name=name,weather_data=weather_data)
    else:
        return redirect("/")
if __name__ == '__main__':
    if not os.path.exists("weather_data"):
        get_city_list()
        with open("weather_data", 'wb') as f:
            f.write(json.dumps(citys_dict).encode("utf-8"))
    else:
        with open("weather_data", 'rb') as f:
            data = f.read().decode("utf-8")
            citys_dict = json.loads(data)
    
    app.run()
