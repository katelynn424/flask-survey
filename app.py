from flask import Flask, request, render_template, flash, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


response_key = "responses"

@app.route('/')
def home_page():
    return render_template('home.html', survey=survey)

@app.route('/begin', methods=["POST"])
def start_survey():
    session[response_key] = []

    return redirect("/questions/0")


@app.route('/questions/<int:id>')
def show_question(id):
    """Display current question"""
    responses = session.get(response_key)

       # make it so you redirect once user completes all questions

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    
    # make it do user cannot manually redirect questions
    if len(responses) != id:
        flash(f"Invalid question id: {id}.")
        return redirect(f"/questions/{len(responses)}")
  


    
    
    question = survey.questions[id]
    return render_template("questions.html", question_num=id, question=question)

 

@app.route('/answer', methods=["POST"])
def handle_answers():

    choice= request.form['answer']
    responses = session[response_key]
    responses.append(choice)
    session[response_key] = responses


    if (len(responses) == len(survey.questions)):
        
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/complete')
def complete():
    """shows completion page"""

    return render_template('complete.html')
