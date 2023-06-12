from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scoreboard.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    guess_team = db.Column(db.String(50), nullable=True)
    guess_score = db.Column(db.String(50), nullable=True)

class ScoreForm(FlaskForm):
    player_name = StringField('Player Name', validators=[DataRequired()])
    score = IntegerField('Score', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    guess_team = StringField('Guess Team')
    guess_score = StringField('Guess Score')
    submit = SubmitField('Add Score')

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class Title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default='Scoreboard')

class TitleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Update Title')

@app.route('/', methods=['GET', 'POST'])
def home():
    category = request.args.get('category')
    if category:
        scores = Score.query.filter_by(category=category).order_by(Score.score.desc()).all()
    else:
        scores = Score.query.order_by(Score.score.desc()).all()
    score_form = ScoreForm()
    delete_forms = [DeleteForm(prefix=str(score.id)) for score in scores]
    
    if score_form.validate_on_submit():
        player_name = score_form.player_name.data
        score_value = score_form.score.data
        category = score_form.category.data
        guess_team = score_form.guess_team.data
        guess_score = score_form.guess_score.data
        new_score = Score(player_name=player_name, score=score_value, category=category)
        db.session.add(new_score)
        db.session.commit()
        return redirect('/')
    
    if request.method == 'POST':
        for score, delete_form in zip(scores, delete_forms):
            if delete_form.validate_on_submit():
                db.session.delete(score)
                db.session.commit()
                return redirect('/')
            
    title = Title.query.first()
    title_form = TitleForm()
    if title_form.validate_on_submit():
        title.title = title_form.title.data
        db.session.commit()
        return redirect('/')
    
    return render_template('scoreboard.html', scores=scores, score_form=score_form, delete_forms=delete_forms, title=title, title_form=title_form)

@app.route('/add', methods=['GET', 'POST'])
def add_score():
    player_name = request.form['player_name']
    score = int(request.form['score'])
    category = request.form['category']
    guess_team = request.form['guess_team']
    guess_score = request.form['guess_score']
    
    new_score = Score(player_name=player_name, score=score, category=category, guess_team=guess_team, guess_score=guess_score)
    db.session.add(new_score)
    db.session.commit()
    
    return redirect('/')

@app.route('/game_result', methods=['POST'])
def game_result():
    winning_team = request.form['winning_team']
    
    # Retrieve all scores
    scores = Score.query.all()
    
    for score in scores:
        # Check if the player's guess matches the winning team
        if score.guess == winning_team:
            score.score += 3  # Increment the score by 3
    
    db.session.commit()
    
    return redirect('/')


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/calculate_scores', methods=['POST'])
def calculate_scores():
    winning_team = request.form['winning_team']
    winning_score = request.form['winning_score']
    
    # Retrieve all scores
    scores = Score.query.all()
    
    for score in scores:
        # Check if the player's guess matches the winning team
        if score.guess_team == winning_team and score.guess_score == winning_score:
            score.score += 5  
        elif score.guess_team == winning_team or score.guess_score == winning_score:
            score.score += 2
        db.session.commit()
    
    return redirect('/')

@app.route('/edit/<int:score_id>', methods=['GET', 'POST'])
def edit_score(score_id):
    score = Score.query.get_or_404(score_id)
    if request.method == 'POST':
        form = ScoreForm(request.form)
        if form.validate():
            score.player_name = form.player_name.data
            score.score = form.score.data
            score.category = form.category.data
            score.guess_team = form.guess_team.data
            score.guess_score = form.guess_score.data
            db.session.commit()
            return redirect('/')
    else:
        form = ScoreForm(obj=score)
    return render_template('edit_score.html', form=form)


@app.route('/delete/<int:score_id>', methods=['POST'])
def delete_score(score_id):
    score = Score.query.get_or_404(score_id)
    db.session.delete(score)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if Title.query.first() is None:
            db.session.add(Title())
            db.session.commit()
    app.run(debug=True, port=5003)
