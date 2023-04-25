from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import re
import time
from csv import DictWriter


app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("vid_index.html")
#writing to file:           
field_names  = ['Video_link','thumbnail', 'Video_title', 'No_views', 'Video_publish']
with open('Youtube.csv', 'a') as f_object:
    dictwriter_object = DictWriter(f_object, fieldnames=field_names)
    dictwriter_object.writeheader()
f_object.close()

@app.route("/review" , methods = ['POST' , 'GET'])
def vid_index():
    if request.method == 'POST':
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
        searchString = request.form['content']
        youtube_url = "https://www.youtube.com/@{}/videos".format(searchString)
        print(youtube_url)
        urlclient = urlopen(youtube_url)
        url_data = urlclient.read()
           
        soup = bs(url_data,'html.parser')
        div_SOUP1 = soup.findAll('script', {})

        temp_list=""
        for i in range(len(div_SOUP1)):
            try:
                if(type(div_SOUP1[i].text.index('"richItemRenderer":'))== int):
                    temp_list+= div_SOUP1[i].text
    
            except:
                pass


        get_text = temp_list.split('"richItemRenderer":')

        del get_text[0]
        my_results =[]
        for i in get_text:
    
            vid_title = (re.findall('"title":{"runs":\[{"text":"(.*?)"', i))
            videoId = re.findall('"videoId":"(.*?)"', i)
            vid_link = ("https://www.youtube.com//watch?v="+str(videoId[0]))
            vid_thumbnail = (re.findall('"thumbnail":{"thumbnails":\[{"url":"(.*?)"', i))
            vid_count = (re.findall('"viewCountText":{"simpleText":"(.*?)"', i))
            vid_pub_time = (re.findall('"publishedTimeText":{"simpleText":"(.*?)"', i))
            result_dict = {"Video_link": vid_link , "thumbnail": vid_thumbnail, "Video_title": vid_title, "No_views": vid_count,
                     "Video_publish": vid_pub_time}
            my_results.append(result_dict)
            with open('Youtube.csv', 'a') as f_object:
                dictwriter_object = DictWriter(f_object, fieldnames=field_names)
                dictwriter_object.writerow(result_dict)
            f_object.close()

        
        try:
            return render_template('vid_result.html', my_results=my_results[0:(len(my_results)-3)])
        except Exception as e:
            print(e)


                  


if __name__=="__main__":
    app.run(host="0.0.0.0", debug=False)