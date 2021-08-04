from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)
app.config["SECRET_KEY"] = "1234567890"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///relationships.db'
db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(100))
    content = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", backref="post_user", lazy=True)

    def __init__(self, title, subtitle, content, user_id):
        self.title = title
        self.subtitle = subtitle
        self.content = content  
        self.user_id = user_id

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email_id = db.Column(db.String(50))
    password = db.Column(db.String(50))
    posts = db.relationship('Post', backref='post', lazy=True)

    def __init__(self, username, email_id, password):
        self.username = username
        self.email_id = email_id
        self.password = password


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/add_post_form' ,methods = ['GET'])
def add_post_form():
    return render_template('add_posts.html')


@app.route('/add_posts' ,methods = ['POST'])
def add_posts():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        content = request.form['content']
        user_id = request.form['user_id']
        my_data = Post(title=title, subtitle=subtitle, content=content, user_id=user_id) 
        db.session.add(my_data)
        db.session.commit()
    posts = Post.query.all()
    
    return render_template('index.html', posts=posts)

@app.route('/update/<id>', methods = ['GET'])
def update(id):
    my_data = Post.query.filter_by(id = id).first()
    return render_template('update.html' ,my_data = my_data)

@app.route('/update_posts/<id>' ,methods = ['POST'])
def update_posts(id):
    if request.method == 'POST':
        my_data = Post.query.filter_by(id = id).first() 
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(my_data)
        my_data.title = request.form['title']
        my_data.subtitle = request.form['subtitle']
        my_data.content = request.form['content']
        db.session.commit()
        return redirect("http://127.0.0.1:5000/", code=302)
        


@app.route('/showdata/<id>', methods = ['GET'])
def showdata(id):
    my_data = User.query.filter_by(id = id).first()


    return render_template('showdata.html' ,my_data = my_data)

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Post.query.filter_by(id = id).first()
    db.session.delete(my_data)
    db.session.commit()

    flash("Post Deleted Successfully")
    return redirect("http://127.0.0.1:5000/", code=302)


@app.route('/show_user/<id>')
def show_user(id):
    user = User.query.filter_by(id = id).first()
    return render_template('show_users.html', user = user)

@app.route('/show_users')
def show_users():
    users = User.query.all()
    return render_template('show_users.html', users = users)

if __name__=="__main__":
   app.run(debug=True)


