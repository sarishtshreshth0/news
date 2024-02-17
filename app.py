from flask import Flask
from flask import render_template, request
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://sarishtshreshth:rvhs2017@cluster0.sf3lhpf.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client['amazon']
my_collection = db['amazon_collection']
app = Flask(__name__)

@app.route('/',methods = ['GET'])
def index():
    return render_template('index.html')

@app.route("/review" , methods = ['POST' , 'GET'])
def result():
    if (request.method == 'POST'):
        searchString = request.form['content'].replace(" ","")
        z=[]
        reviews = []
        url="https://www.amazon.in/s?k=" + searchString
        html_url=urlopen(url).read()
        html_box = bs(html_url,'html.parser')
        for i in range(22):
            a = str(i)
            try:
                element = html_box.find_all("div", {"data-index": a})[0].span.div.div.div.div.div.a
                if element:
                    href_value = element.get('href')
                    if href_value:
                        z.append(href_value)
                        #print(href_value)
                    else:
                        continue
                else:
                    continue
            
            except Exception as e:
                pass
        for i in range(len(z)):
            s=z[i].split('/')
            data = {'product_name':s[1]}
            my_collection.insert_one(data)
            reviews.append(data)
    return render_template("results.html",reviews=reviews[0:(len(reviews)-1)])
    
if __name__=="__main__":
    app.run(host="0.0.0.0")
