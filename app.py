from flask import Flask, render_template, request, session, redirect, send_file, url_for
from pymongo import MongoClient
from fpdf import FPDF
import matplotlib.pyplot as plt
import os
import secrets
from datetime import datetime
from flask_pymongo import PyMongo
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import bcrypt


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/incident_response_db"  # Make sure this URI is correct
mongo = PyMongo(app)
app.secret_key = secrets.token_hex(16)

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['incident_response_db']
users_collection = db['users']
incidents_collection = db['incidents']
scores_collection = db['scores']

# Static Phishing Email Images
images = ["Picture1.jpg", "Picture2.jpg", "Picture3.jpg", "Picture4.jpg", "Picture5.jpg", "Picture6.jpg", "Picture7.jpg"]
correct_answers = {
    "Picture1.jpg": "legitimate",
    "Picture2.jpg": "phishing",
    "Picture3.jpg": "phishing",
    "Picture4.jpg": "legitimate",
    "Picture5.jpg": "phishing",
    "Picture6.jpg": "legitimate",
    "Picture7.jpg": "phishing"
}

def log_event(event):
    db['timeline'].insert_one({
        'username': session['username'],
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'event': event
    })

# Helper function to check if user is logged in
def is_logged_in():
    return 'username' in session

# Helper function to fetch incidents by difficulty
def get_incidents_by_difficulty(difficulty):
    return list(incidents_collection.find({'difficulty': difficulty}))

def update_score(username, points):
    # Find the user score document
    score_entry = mongo.db.scores.find_one({'username': username})

    if score_entry:
        # Increment the score
        new_score = score_entry['score'] + points
        mongo.db.scores.update_one(
            {'username': username},
            {'$set': {'score': new_score}}
        )
    else:
        # If no score entry exists, create one with the initial points
        mongo.db.scores.insert_one({'username': username, 'score': points})

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if is_logged_in():
#         return redirect(url_for('dashboard'))
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if users_collection.find_one({'username': username}):
#             return "Username already exists!"
#         user = {'username': username, 'password': password, 'scores': []}
#         users_collection.insert_one(user)
#         return redirect('/login')
#     return render_template('register.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if is_logged_in():
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username already exists
        if users_collection.find_one({'username': username}):
            return "Username already exists!"
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Store the user with the hashed password
        user = {'username': username, 'password': hashed_password, 'scores': []}
        users_collection.insert_one(user)
        return redirect('/login')
    return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if is_logged_in():
#         return redirect('/dashboard')
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = users_collection.find_one({'username': username, 'password': password})
#         if user:
#             session['username'] = username
#             return redirect('/dashboard')
#         else:
#             return "Invalid credentials"
#     return render_template('login.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect('/dashboard')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Find the user by username
        user = users_collection.find_one({'username': username})
        
        if user:
            # Check if the provided password matches the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                # Password is correct, log the user in
                session['username'] = username
                return redirect('/dashboard')
            else:
                return "Invalid credentials"
        else:
            return "Invalid credentials"
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect('/')
    user = users_collection.find_one({'username': session['username']})
    user_scores = user.get('scores', [])
    avg_score = sum(user_scores) / len(user_scores) if user_scores else 0
    return render_template('dashboard.html', username=session['username'], avg_score=avg_score)

# @app.route('/simulate', methods=['GET', 'POST'])
# def simulate():
#     if not is_logged_in():
#         return redirect('/')

#     if request.method == 'POST':
#         difficulty = request.form['difficulty']
#         incidents = get_incidents_by_difficulty(difficulty)

#         # Limit to the first 10 incidents
#         session['incidents'] = incidents[:10]  
#         session['current_simulation_index'] = 0
#         session['difficulty'] = difficulty
#         return redirect(url_for('show_simulation'))

#     return render_template('difficulty.html')
@app.route('/simulate', methods=['GET', 'POST'])
def simulate():
    if not is_logged_in():
        return redirect('/login')

    if request.method == 'POST':
        # Check if this is the POST request for difficulty selection
        if 'difficulty' in request.form:
            difficulty = request.form['difficulty']
            incidents = get_incidents_by_difficulty(difficulty)

            # Limit to the first 10 incidents
            session['incidents'] = incidents[:10]  
            session['current_simulation_index'] = 0
            session['difficulty'] = difficulty
            return redirect(url_for('show_simulation'))

        # Check if this is the POST request for submitting answers (simulation logic)
        if 'answers' in request.form:
            username = session['username']
            user_answers = request.form.getlist('answers')  # User's answers from form
            correct_answers = get_correct_answers()  # Logic to retrieve correct answers

            score = 0
            for user_answer, correct_answer in zip(user_answers, correct_answers):
                if user_answer == correct_answer:
                    score += 10  # Example: 10 points for correct answers
                else:
                    score -= 5  # Subtract 5 for incorrect answers

            # Update score using the update_score function
            update_score(username, score)

            return redirect('/dashboard')

    return render_template('difficulty.html')


@app.route('/simulation')
def show_simulation():
    if not is_logged_in():
        return redirect('/')

    current_index = session.get('current_simulation_index', 0)
    incidents = session.get('incidents', [])

    if current_index >= len(incidents):
        return render_template('result.html', result="All simulations completed", try_again=True)

    incident = incidents[current_index]
    return render_template('simulate.html', incident=incident, current_index=current_index + 1, total=len(incidents))

@app.route('/submit_response', methods=['POST'])
def submit_response():
    if not is_logged_in():
        return redirect('/')

    selected_option = request.form['response']
    current_index = session['current_simulation_index']
    incidents = session['incidents']
    incident = incidents[current_index]

    correct_option = incident['correct_option']
    user = users_collection.find_one({'username': session['username']})

    # Determine score based on user's response
    if selected_option == correct_option:
        score = 10
        result = "Correct! You chose the best response."
        log_event('User completed a simulation successfully')  # Log success event
    else:
        score = 0
        result = f"Incorrect. The best response was: {correct_option}"
        log_event('User completed a simulation unsuccessfully')  # Log failure event

    # Save score to scores collection for leaderboard
    scores_collection.insert_one({'username': session['username'], 'score': score, 'date': datetime.now()})

    # Also update user-specific score list
    users_collection.update_one(
        {'username': session['username']},
        {'$push': {'scores': score}}
    )

    session['current_simulation_index'] += 1

    if session['current_simulation_index'] < len(incidents):
        return render_template('result.html', result=result, next_simulation=True)
    else:
        # Log the event of completing the simulation
        log_event('User completed all simulations for this level')  # Log completion event
        return render_template('result.html', result=result, try_again=True)

# Phishing simulation route
@app.route('/simulate_phishing', methods=['GET', 'POST'])
def simulate_phishing():
    if not is_logged_in():
        return redirect('/login')

    if request.method == 'POST':
        user_answers = request.form.getlist('phishing_email')
        score = 0

        # Calculate score based on user's answers
        for i, img in enumerate(images):
            user_answer = request.form[f'phishing_email_{i+1}']
            if user_answer == correct_answers[img]:
                score += 1

        # Store the score in the session
        session['phishing_score'] = score
        return redirect(url_for('phishing_result'))

    # If GET request, show the phishing images
    return render_template('phishing_simulation.html', images=images)

# Result page for phishing simulation
@app.route('/phishing_result')
def phishing_result():
    if not is_logged_in():
        return redirect('/login')

    score = session.get('phishing_score', 0)
    total = len(images)  # Total number of phishing email images
    return render_template('phishing_result.html', score=score, total=total)


# Route to download PDF explanation
@app.route('/download_pdf')
def download_pdf():
    return send_file('static/pdf/Model Answer - Task 1 (annotated version).pdf', as_attachment=True)

@app.route('/report')
def report():
    if not is_logged_in():
        return redirect('/')
    user = users_collection.find_one({'username': session['username']})
    scores = user.get('scores', [])
    avg_score = sum(scores) / len(scores) if scores else 0

    if scores:
        plt.figure()
        plt.plot(range(1, len(scores) + 1), scores, marker='o')
        plt.title('Score Progression')
        plt.xlabel('Attempt')
        plt.ylabel('Score')
        plt.savefig('static/images/score_progression.png')
        plt.close()
    return render_template('report.html', avg_score=avg_score)

@app.route('/generate_report')
def generate_report():
    if not is_logged_in():
        return redirect('/')
    user = users_collection.find_one({'username': session['username']})
    scores = user.get('scores', [])
    avg_score = sum(scores) / len(scores) if scores else 0

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Incident Response Report for {session['username']}", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Average Score: {avg_score}", ln=True)
    pdf.cell(0, 10, f"Total Attempts: {len(scores)}", ln=True)

    if scores:
        pdf.cell(0, 10, "Score Progression:", ln=True)
        pdf.image('static/images/score_progression.png', x=10, y=50, w=190)

    report_path = os.path.join('static', 'reports', f"{session['username']}_report.pdf")
    pdf.output(report_path)
    return send_file(report_path, as_attachment=True)

@app.route('/playbook')
def playbook():
    if not is_logged_in():
        return redirect('/')
    return render_template('playbook.html')

@app.route('/resources')
def resources():
    if not is_logged_in():
        return redirect('/')
    return render_template('resources.html')

@app.route('/glossary')
def glossary():
    if not is_logged_in():
        return redirect('/')
    return render_template('glossary.html')

# @app.route('/leaderboard')
# def leaderboard():
#     if not is_logged_in():
#         return redirect('/')

#     top_scores = scores_collection.find().sort('score', -1).limit(10)
#     return render_template('leaderboard.html', top_scores=top_scores)

# @app.route('/leaderboard')
# def leaderboard():
#     if not is_logged_in():
#         return redirect('/')
    
#     try:
#         # Fetch scores from MongoDB and convert the cursor to a list
#         scores_cursor = mongo.db.scores.find().sort('score', -1)
#         scores = list(scores_cursor)  # Convert Cursor to a list
#         return render_template('leaderboard.html', scores=scores)
#     except Exception as e:
#         print(f"Error fetching scores: {str(e)}")  # Log the error for debugging
#         return render_template('error.html', message="An error occurred while fetching scores.")
# @app.route('/leaderboard')
# def leaderboard():
#     if not is_logged_in():
#         return redirect('/')

#     try:
#         # Aggregate scores by username, getting the maximum score for each user
#         scores_cursor = mongo.db.scores.aggregate([
#             {
#                 '$group': {
#                     '_id': '$username',  # Group by username
#                     'max_score': {'$max': '$score'}  # Get the maximum score for each user
#                 }
#             },
#             {
#                 '$sort': {'max_score': -1}  # Sort by max score in descending order
#             }
#         ])

#         # Convert the cursor to a list
#         scores = [{ 'username': score['_id'], 'score': score['max_score'] } for score in scores_cursor]

#         # Debug: Print the fetched scores
#         print("Fetched scores:", scores)

#         return render_template('leaderboard.html', scores=scores)
#     except Exception as e:
#         print(f"Error fetching scores: {str(e)}")  # Log the error for debugging
#         return render_template('error.html', message="An error occurred while fetching scores.")

# @app.route('/leaderboard')
# def leaderboard():
#     if not is_logged_in():
#         return redirect('/')

#     try:
#         # Aggregate scores by username, getting the average score for each user
#         scores_cursor = mongo.db.scores.aggregate([
#             {
#                 '$group': {
#                     '_id': '$username',  # Group by username
#                     'avg_score': {'$avg': '$score'}  # Get the average score for each user
#                 }
#             },
#             {
#                 '$sort': {'avg_score': -1}  # Sort by average score in descending order
#             }
#         ])

#         # Convert the cursor to a list
#         scores = [{ 'username': score['_id'], 'score': round(score['avg_score'], 2) } for score in scores_cursor]

#         # Debug: Print the fetched scores
#         print("Fetched scores:", scores)

#         return render_template('leaderboard.html', scores=scores)
#     except Exception as e:
#         print(f"Error fetching scores: {str(e)}")  # Log the error for debugging
#         return render_template('error.html', message="An error occurred while fetching scores.")

@app.route('/leaderboard')
def leaderboard():
    if not is_logged_in():
        return redirect('/')

    try:
        # Aggregate scores by username, getting the average score for each user
        scores_cursor = mongo.db.scores.aggregate([
            {
                '$group': {
                    '_id': '$username',  # Group by username
                    'avg_score': {'$avg': '$score'}  # Get the average score for each user
                }
            },
            {
                '$sort': {'avg_score': -1}  # Sort by average score in descending order
            }
        ])

        # Convert the cursor to a list
        scores = [{ 'username': score['_id'], 'score': round(score['avg_score'], 2) } for score in scores_cursor]

        # Debug: Print the fetched scores
        print("Fetched scores:", scores)

        return render_template('leaderboard.html', scores=scores)
    except Exception as e:
        print(f"Error fetching scores: {str(e)}")  # Log the error for debugging
        return render_template('error.html', message="An error occurred while fetching scores.")



@app.route('/recommendations')
def recommendations():
    if not is_logged_in():
        return redirect('/')
    recommendations = [
        "Review the Incident Response Playbook.",
        "Explore more resources in the Resource Library.",
        "Practice with more difficult scenarios."
    ]
    return render_template('recommendations.html', recommendations=recommendations)

# @app.route('/timeline')
# def timeline():
#     if not is_logged_in():
#         return redirect('/')
#     user_timeline = db['timeline'].find({'username': session['username']}).sort('time', -1)
#     return render_template('timeline.html', timeline=user_timeline)
@app.route('/timeline')
def timeline():
    if not is_logged_in():
        return redirect('/')
    events = list(mongo.db.timeline.find().sort('time', -1))  # Convert Cursor to a list
    print("Number of events:", len(events))  # Print the number of events for debugging
    return render_template('timeline.html', events=events)

@app.route('/nist_guidance')
def nist_guidance():
    if not is_logged_in():
        return redirect('/')
    nist_data = {
        'Identify': 'Develop an organizational understanding...',
        'Protect': 'Develop and implement appropriate safeguards...',
        'Detect': 'Develop and implement appropriate activities to identify...',
        'Respond': 'Develop and implement appropriate activities to take action...',
        'Recover': 'Develop and implement appropriate activities to maintain plans...'
    }
    return render_template('nist_guidance.html', guidance=nist_data)

if __name__ == "__main__":
    app.run(debug=True)
