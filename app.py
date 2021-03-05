from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def index():
    """prompts which survey user wants"""

    return render_template("survey_choice.html", survey_type=surveys)

@app.route("/start", methods=["POST"])
def start():
    """Shows title, instructions, and button to route to survey questions"""
    survey_type = request.form['survey']
    title = surveys[survey_type].title
    instructions = surveys[survey_type].instructions
    session['responses'] = []
    session['survey'] = survey_type
    return render_template("survey_start.html", title=title, instructions=instructions)

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
    survey = surveys[session['survey']]
    print(survey)
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
