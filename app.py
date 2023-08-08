from flask import Flask , render_template,request 
import requests
import pandas as pd
import numpy as np
import pickle
app = Flask(__name__)

# def recommend(movie):
#     idx= new_movies[new_movies.title==movie].index[0]
#     dis= similarity[idx]
#     movie_lst=sorted(list(enumerate(dis)),reverse=True,key=lambda x:x[1])[:5]
    
#     return new_movies.iloc[[i[0] for i in movie_lst]]


def recommend(movie):
    idx= new_movies[new_movies.title==movie].index[0]
    dis= similarity[idx]
    movie_lst=sorted(list(enumerate(dis)),reverse=True,key=lambda x:x[1])[:5]
    new_m=new_movies.iloc[[i[0] for i in movie_lst]].copy()
    
    img=[]
    for i in new_m.id:
        url = f"https://api.themoviedb.org/3/movie/{i}?api_key=e5bcbe1499e861996dcce506f469259e"
        response = requests.get(url)
        data=response.json()
        try:
            img.append(data['poster_path'])
        except:
            img.append(None)
    new_m['img']=img
    return new_m

new_movies=pickle.load(open('new_movies.pkl','rb'))
new_movies=pd.DataFrame(new_movies)
similarity=pickle.load(open('similarity.pkl','rb'))





@app.route("/")
def index():
    m=np.array(new_movies.sort_values('title'))
    return render_template('index.html',title='Movie Recommendation',m=m)

@app.route("/movie/<movie>")
def pred(movie):    
    movies=recommend(movie)
    id=np.array(new_movies[new_movies.title==movie]['id'])[0]
    url = f"https://api.themoviedb.org/3/movie/{id}?api_key=e5bcbe1499e861996dcce506f469259e"
    print(url)
    response = requests.get(url)
    m_data=response.json()
    return render_template('movies.html',title=movie,movies=np.array(movies),m_data=m_data)



if __name__=="__main__":
    app.run(debug=True)