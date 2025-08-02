from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# --- Setup Instructions ---
# 1. Install Flask and Flask-SQLAlchemy:
#    pip install Flask Flask-SQLAlchemy
# 2. To run the app, save this code as app.py.
# 3. Save the HTML files (index.html and edit.html) into a directory named 'templates'.
# 4. Open a terminal in the same directory and run:
#    flask --app app.py run

app = Flask(__name__)

# --- Database Configuration ---
# Using a simple SQLite database for this example.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database Model ---
# This class defines the structure of our 'Review' table in the database.
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Review {self.id}>'

# --- Routes ---

# Main page: displays all reviews and a form to add a new one.
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get data from the form
        author = request.form.get('author')
        text = request.form.get('text')
        
        # Create a new Review object and add it to the database
        new_review = Review(author=author, text=text)
        try:
            db.session.add(new_review)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue adding your review.'
    else:
        # Retrieve all reviews from the database
        reviews = Review.query.order_by(Review.created_at.desc()).all()
        return render_template('index.html', reviews=reviews)

# Update a specific review
@app.route('/update/<int:review_id>', methods=['GET', 'POST'])
def update(review_id):
    review_to_update = Review.query.get_or_404(review_id)
    
    if request.method == 'POST':
        # Update the review with new form data
        review_to_update.author = request.form.get('author')
        review_to_update.text = request.form.get('text')
        
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue updating your review.'
    else:
        return render_template('edit.html', review=review_to_update)

# Delete a specific review
@app.route('/delete/<int:review_id>')
def delete(review_id):
    review_to_delete = Review.query.get_or_404(review_id)
    
    try:
        db.session.delete(review_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'There was an issue deleting that review.'

# --- Main Entry Point ---
# This block creates the database and runs the application.
if __name__ == '__main__':
    with app.app_context():
        # This will create the database file and table if it doesn't exist
        db.create_all()
    # The 'flask run' command is recommended for production.
    # This is for development purposes only.
    app.run(debug=True)

