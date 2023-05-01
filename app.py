from flask import Flask, flash, redirect, render_template, request, session
from helpers import suggest


# Configure application
app = Flask(__name__)

@app.route("/")
def index():
    list_moods = ['Hype', 'Sad', 'Cheerful', 'Chill']
    return render_template("index.html", list_moods=list_moods)

@app.route("/recommendations", methods=["GET", "POST"])
def recommend():
    if request.method == "POST":
        # Defines variables
        year = request.form.get("year")
        genre = request.form.get("genre")
        length = int(request.form.get("length"))
        mood = request.form.get("mood")

        if mood == 'Hype':
            # Defining boundaries for 'Hype'
            acoustic = 0
            Acoustic = 0.4
            dance = 0.3
            Dance = 1
            energy = 0.6
            Energy = 1
            valence = 0
            Valence = 1
        elif mood == 'Sad':
            # Defining boundaries for 'Sad'
            acoustic = 0.4
            Acoustic = 1
            dance = 0
            Dance = 0.5
            energy = 0
            Energy = 0.5
            valence = 0
            Valence = 0.5
        elif mood == 'Cheerful':
            # Defining boundaries for 'Cheerful'
            acoustic = 0
            Acoustic = 1
            dance = 0.4
            Dance = 1
            energy = 0.3
            Energy = 1
            valence = 0.5
            Valence = 1
        elif mood == 'Chill':
            # Defining boundaries for 'Chill'
            acoustic = 0.5
            Acoustic = 1
            dance = 0
            Dance = 0.5
            energy = 0
            Energy = 0.5
            valence = 0.3
            Valence = 1

        suggestion = suggest(genre, year, length, acoustic, dance, energy, valence, Acoustic, Dance, Energy, Valence)
        recommend = zip(suggestion[0], suggestion[1])
        return render_template("recommendations.html", recommend=recommend)
    else:
        return redirect("/")
