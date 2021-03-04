from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def index():
    """Shows title, instructions, and button to route to survey questions"""
    session["responses"] = []

    return render_template("survey_start.html", title=survey.title, instructions=survey.instructions)

@app.route("/begin", methods=["POST"])
def begin():
    """routes to survey questions"""

    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def answer():
    """ gets the responses and redirects to next question """
    responses = session['responses']
    responses.append(request.form['choice'])
    session['responses'] = responses
    num = len(responses)

    if (num == len(survey.questions)):
        return redirect("/thankyou")

    return redirect(f"/questions/{num}")

@app.route("/questions/<int:qnum>")
def questions(qnum):
    """populates page with survey questions"""
    num_answered = len(session['responses'])
    if (num_answered == len(survey.questions)):
        flash("Yo, you can't go there!")
        return redirect("/thankyou")
    elif (qnum != num_answered):
        flash("Yo, you can't go there!!!")
        return redirect(f"/questions/{num_answered}")

    question = survey.questions[qnum]
    print("this is question:", question)

    return render_template("question.html", question=question)

@app.route("/thankyou")
def thanks():
    """ thank you page """

    return render_template("completion.html")
