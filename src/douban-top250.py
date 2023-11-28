#-*- coding:utf-8 -*-

import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
}

index = 0

output = {}

while True:
    url = f"https://movie.douban.com/top250?start={index * 25}&filter="
    index += 1
    with requests.get(url=url, headers=headers) as resp:

        ol = re.findall(r'<ol class="grid_view">.*</ol>', resp.text, re.DOTALL)
        lis = re.findall(r'<li[^>]*>(.*?)</li>', ol[0], re.DOTALL)

        if len(lis) == 0:
            print(0)
            break

        for movie in lis:
            move_names_text = re.findall(r'<span class="title">(.*?)</span>', movie, re.DOTALL)
            person_names_text = re.findall(r'<p class="">\n(.*?)<br>', movie, re.DOTALL)
            year_country_text = re.findall(r'<br>\n(.*?)</p>', movie, re.DOTALL)
            year = re.findall(r'\d+', year_country_text[0], re.DOTALL)[0]
            country = re.findall(r'/&nbsp;(.*?)&nbsp;/', year_country_text[0], re.DOTALL)
            rating_score = re.findall(r'<span class="rating_num" property="v:average">(.*?)</span>', movie, re.DOTALL)
            chinese_movie_name = move_names_text[0]
            director_name = re.findall(r'导演: (.*?)&', person_names_text[0], re.DOTALL)
            types = re.findall(r'/&nbsp;([^/]+)\n', year_country_text[0])[-1].split(" ")

            information = {
                "DirectorName": director_name,
                "RatingScore": rating_score[0],
                "PublishYear": year,
                "PublishCountry": country[0],
                "Type": types,
            }
            output[chinese_movie_name] = information

with open("../output/top250.txt", "w", encoding="utf-8") as file:
    file.write(str(output))