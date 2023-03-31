from app import app,db
import flask,requests,bs4,datetime,json
from bs4 import BeautifulSoup
from bson.objectid import ObjectId


@app.route('/add_data')
def add_data():
    db.todos.insert_one({'title': "Harry Potter", 'body': "written by J.K.Rowling"})
    return flask.jsonify(message="Successfully added the data")


@app.route("/show_data")
def show_data():
   
    todos = db.todos.find_one()  
    data = {'_id': str(todos['_id']), 'list': todos['list']}

    return flask.jsonify(data)
    #return flask.jsonify([todo for todo in todos])

@app.route("/delete_data")
def delete_data():
    result = db.todos.delete_one({"_id": ObjectId("6426817f7d3a34a08d6c4c4b")})
    return "Deleted document count: {}".format(result.deleted_count)

@app.route("/update_data")
def update_data():
    data_id = {"_id": ObjectId("64258a561be5412448a12205")}
    todos = db.todos.find_one(data_id)
    
    oldstr = todos["list"][1]["News_article_2"]                     # want to modify this data 
    Modifystr =  "Some update"                                      # update data with new one

    todos["list"][1]["News_article_2"] = Modifystr

    result = db.todos.update_one(data_id, {"$set": todos})

    if result.modified_count == 1:
        return f"Data updated successfully\nChanges made: {oldstr} --> {Modifystr}"

    else:
        return "Failed to update data"




@app.route('/scrape')
def scrape():

    url = "https://www.bbc.com"  
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content, 'lxml')
    count = 1
    News_articles = []
    author_articles_collection = {}

    for headlinedata_link in soup.select('.block-link__overlay-link'):
                
        headline = headlinedata_link.text.strip()            # headline text     
        
        headline_url = ''
        if headlinedata_link['href'].startswith('http'):
            headline_url = headlinedata_link['href']
        else:
            headline_url = str(url+headlinedata_link['href'])                        # headline url
        

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
      
        if author_name not in author_articles_collection and author_name != "Unknown" :
             author_articles_collection[author_name] = []
        
        if author_name != "Unknown" :
             author_articles_collection[author_name].append(headline_url)


        
        

        time_elem = soup_1.find('time', {'data-testid': 'timestamp'})
        if time_elem is None:
            date = "Unknown"
            time = "Unknown"
    
        else:
            datetime_str = time_elem.get('datetime')
            dt = datetime.datetime.fromisoformat(datetime_str[:-1]) 
            date  = dt.date()                                        

            time  = dt.time()

        
        News_article = {f"News_article_{count}" : headline , "Article URL" : headline_url , "Author name" : author_name, "Publication Date" : str(date), "Time" : str(time)}
         
        News_articles.append(News_article) 
        if count==15:
            data = {"articles collection":News_articles,"authors publications": author_articles_collection}
            db.todos.insert_one(data)
            return 'Scraped and stored article data!'
        count+=1 
   
        


                

   
                  

                

