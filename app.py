from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('model/popular.pkl', 'rb'))
pt = pickle.load(open('model/pt.pkl', 'rb'))
books = pickle.load(open('model/books.pkl', 'rb'))
similarity_scores = pickle.load(open('model/similarity_scores.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('top20.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('top20.html')


def get_classes(classes):
    if classes == "Horror":
        return("Silence of the Lambs")
    elif classes == "Fantasy":
        return("The Fellowship of the Ring (The Lord of the Rings, Part 1)")
    elif classes == "Mistery":
        return("The Testament")
    elif classes == "Romance":
        return("The Da Vinci Code")
    elif classes == "Action":
        return("The Catcher in the Rye")
    elif classes == "Adventure":
        return("The Kitchen God's Wife")
    elif classes == "Fanfiction":
        return("The Tale of the Body Thief (Vampire Chronicles (Paperback))")
    elif classes == "History":
        return("Clara Callan")
    elif classes == "Thriller":
        return("Pleading Guilty")
    elif classes == "ClassicRomance":
        return("Pride and Prejudice")
    elif classes == "Genre":
        return("Pride and Prejudice")


@app.route('/recommend', methods=['post'])
def recommend():
    user_input = request.form.get('genre')
    genre = get_classes(user_input)
    index = np.where(pt.index == genre)[0][0]
    similar_items = sorted(
        list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:11]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates(
            'Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates(
            'Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates(
            'Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommendation.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
