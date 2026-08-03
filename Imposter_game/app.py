from flask import Flask, render_template, request, redirect, url_for, session
import random


app = Flask(__name__)

app.secret_key = "imposter_secret_key"


@app.route("/")
def index():

    return render_template("index.html")



@app.route("/start", methods=["POST"])
def start():

    players = int(request.form["players"])
    topic = request.form["topic"]


    roles = [topic] * (players - 1)

    roles.append("Imposter")

    random.shuffle(roles)


    session["players"] = players
    session["roles"] = roles
    session["current"] = 0
    session["results"] = []


    return redirect(url_for("reveal"))




@app.route("/reveal")
def reveal():

    current = session["current"]
    players = session["players"]


    if current >= players:

        return redirect(url_for("password"))


    return render_template(
        "reveal.html",
        player=current+1
    )




@app.route("/show_role")
def show_role():

    current = session["current"]

    role = session["roles"][current]


    session["results"].append(
        f"Player {current+1} : {role}"
    )


    session["current"] += 1


    return render_template(
        "role.html",
        role=role
    )





@app.route("/next")
def next_player():

    if session["current"] < session["players"]:

        return redirect(url_for("reveal"))

    else:

        return redirect(url_for("password"))




@app.route("/password", methods=["GET","POST"])
def password():

    if request.method=="POST":

        pwd=request.form["password"]


        if pwd=="1234":

            return redirect(url_for("result"))


    return render_template("password.html")





@app.route("/result")
def result():

    return render_template(
        "result.html",
        results=session["results"]
    )





@app.route("/new")
def new_game():

    session.clear()

    return redirect(url_for("index"))




# if __name__=="__main__":
#     app.run(debug=True, host="0.0.0.0")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)