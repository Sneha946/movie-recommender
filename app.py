from flask import Flask, render_template, request
import pickle
import requests

app = Flask(__name__)

# Load movie data and similarity matrix
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# OMDb API key (Replace with your actual API key)
OMDB_API_KEY = '902bbfc'
OMDB_URL = "http://www.omdbapi.com/"


def fetch_poster(movie_title):
    """Fetches the movie poster URL from the OMDb API."""
    params = {
        't': movie_title,
        'apikey': OMDB_API_KEY
    }
    response = requests.get(OMDB_URL, params=params)
    data = response.json()

    # Check if a valid poster exists
    if 'Poster' in data and data['Poster'] != "N/A":
        return data['Poster']
    return None  # Return None if no valid poster found


@app.route('/', methods=['GET', 'POST'])
def home():
    movie_titles = movies['title'].tolist()
    recommendations = []  # Default to an empty list

    if request.method == 'POST':
        # Get the selected movie
        selected_movie = request.form['movie']
        # Find the index of the selected movie
        movie_index = movies[movies['title'] == selected_movie].index[0]
        # Find the top 5 similar movies
        similarity_scores = list(enumerate(similarity[movie_index]))
        sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Get recommended movies and their posters
        recommendations = []
        for i in sorted_scores[1:6]:  # Get top 5 recommended movies
            movie_title = movies.iloc[i[0]]['title']
            poster_url = fetch_poster(movie_title)
            recommendations.append((movie_title, poster_url))  # Store both title and poster

        return render_template('index.html', movies=movie_titles, selected_movie=selected_movie,
                               recommendations=recommendations)

    return render_template('index.html', movies=movie_titles, recommendations=recommendations)


if __name__ == '__main__':
    app.run(debug=True)
