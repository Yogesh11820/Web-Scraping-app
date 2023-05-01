from app import app
import flask,requests,bs4,datetime,json
from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from app import mongo
from pymongo.errors import PyMongoError
from flask import render_template



@app.route('/frontpage')
def frontpage():
    return render_template('frontpage.html')



@app.route('/scrape')
def scrape():

    url = "https://www.bbc.com"  
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content, 'lxml')
    count = 1
    News_articles = []

    if mongo.db.articles.count_documents({}) == 0 : 
       mongo.db.articles.insert_one({'Author_Collections' : []})

    for headlinedata_link in soup.select('.block-link__overlay-link'):
                
        headline = headlinedata_link.text.strip()                # headline text     
        
        ispresent = mongo.db.articles.count_documents({'News Article Collections.News article headline': headline})
        #print(ispresent)      # headline check in database

        
        if not ispresent:        
                    headline_url = ''
                    if headlinedata_link['href'].startswith('http'):
                        headline_url = headlinedata_link['href']
                    else:
                        headline_url = str(url+headlinedata_link['href'])      # headline url
                    

                    req = requests.get(headline_url)
                    soup_1 = bs4.BeautifulSoup(req.content,'lxml')
                    
                    
                    author_element = soup_1.select_one('.ssrcss-68pt20-Text-TextContributorName')

                    if author_element is None:
                                author_element = soup_1.select_one('.lx-commentary__meta-reporter ')

                                if author_element is None:
                                    author_name = "Unknown"
                                else:
                                    author_name = author_element.text.strip()
                    else:
                        author_name = author_element.text.strip()

                    author_name = author_name.split("By")[-1].strip()

                    if  mongo.db.articles.count_documents({f'Author_Collections.{author_name}': {'$exists': True}}):
                             mongo.db.articles.update_one({f'Author_Collections.{author_name}': {'$exists': True}},{'$addToSet': {f'Author_Collections.$.{author_name}': headline_url}})

                    elif author_name != 'Unknown' : 
                         mongo.db.articles.update_one({}, {'$push': {'Author_Collections': {author_name : [headline_url]}}})



                    time_elem = soup_1.find('time', {'data-testid': 'timestamp'})
                    if time_elem is None:
                        date = "Unknown"
                        time = "Unknown"
                
                    else:
                        datetime_str = time_elem.get('datetime')
                        dt = datetime.datetime.fromisoformat(datetime_str[:-1]) 
                        date  = dt.date()                                        

                        time  = dt.time()

        
                    News_article = {"News article headline" : headline , "Article URL" : headline_url , "Author name" : author_name, "Publication Date" : str(date), "Time" : str(time)}
                    News_articles.append(News_article) 

       
        if count==5:

            if mongo.db.articles.count_documents({})==0 :
                data = {"News Article Collections":News_articles} 
                
                mongo.db.articles.insert_one(data)
                

            elif len(News_articles):
                
                 mongo.db.articles.update_one({},{'$push' : {'News Article Collections':{'$each':News_articles}}})

            
            return render_template('success.html')
        count+=1 
   
        


                

   
                  

                





