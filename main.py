from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Blog123@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key='y337kGcys&zP3B'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(5000))
    owner_id = db.Column(db.String(20), db.ForeignKey('user.username'))

    def __init__(self, title, body, user):
        self.title = title
        self.body = body
        self.user = user


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    Posts = db.relationship('Blog', backref='user')
    

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['/login','/signup','/blog','/','/logout']
    if request.path not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/', methods=['POST', 'GET'])
def index():
    
    names = User.query.all()

    return render_template('index.html', title="Blogz", authors= names)



@app.route('/blog', methods=['POST', 'GET'])
def Posts():

    name = request.args.get('id')
    blogger = request.args.get('username')
    post = request.args.get('post')

    if not name and not blogger and not post:
        blogs = Blog.query.all()
        

        return render_template('Allposts.html',title="Blogz", blogs=blogs)

    if blogger:

        cases = Blog.query.filter_by(owner_id= blogger).all()
       
        return render_template('singleUser.html', title= blogger, writer= blogger, cases= cases)
    
    if post:

        story= Blog.query.filter_by(title= post).first()
        return render_template('Myblog.html', title= post, Btitle= story.title, your_blog= story.body, blogger= story.owner_id)
    
    else:
        
        Postings = Blog.query.filter_by(owner_id=name).first()
        author_name = User.query.filter_by(username=name).first()
        return render_template('Myblog.html', title= name, Btitle = Postings.title, your_blog= Postings.body)

    

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    
    if request.method == 'POST':
        
        blog_name = request.form['blog_title']
        blog_body = request.form['blog']
        user = User.query.filter_by(username= session['username']).first()
        
        if not blog_name:
            return render_template('Postentry.html', title="Add a Blog Entry", title_error="Please insert a title", blog= blog_body)
        if not blog_body:
            return render_template('Postentry.html', title="Add a Blog Entry", blog_error="Please insert a blog", blog_title= blog_name)
        else:

            new_blog = Blog(blog_name,blog_body,user)
            db.session.add(new_blog)
            db.session.commit()
 
           
   
            return redirect('/blog?post={}'.format(blog_name))

    return render_template('Postentry.html',title="Add a Blog Entry")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        passcode = request.form['password']

        user = User.query.filter_by(username= username).first()

        if not username:
            return render_template('login.html', title= 'Blogz-login', username_error="Please enter a valid username")
    
        if ' ' in  username:
            return render_template('login.html', title= 'Blogz-login', username_error="No spaces in username please")

        if len(username) < 3 or len(username) > 20:
            return render_template('login.html', title= 'Blogz-login', username_error="Username must be between 3 and 20 characters", username= username)

        if not passcode:
            return render_template('login.html', title= 'Blogz-login', password_error="Please enter password", username= username)

        if len(passcode) < 3 or len(passcode) > 20:
            return render_template('login.html', title= 'Blogz-login', password_error="Password must be between 3 and 20 characters", username= username)

        if ' ' in passcode:
            return render_template('login.html', title= 'Blogz-login', password_error="Passwords have no spaces please", username= username)

        else:
            if user and user.password == passcode:
                session['username'] = username
           
                return redirect('/newpost')

            else:
                return render_template('login.html', title= 'Blogz-login', username_error= 'User password incorrect, or user does not exist')

    return render_template('login.html', title= 'Blogz-login')


@app.route("/signup", methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':

        username= request.form['username']
        passcode= request.form['password']
        recode= request.form['re_password']

        

        if not username:
            return render_template('signup.html', title= 'Blogz-signup', username_error="Please enter a valid username")
    
        if ' ' in  username:
            return render_template('signup.html', title= 'Blogz-signup', username_error="No spaces in username please")

        if len(username) < 3 or len(username) > 20:
            return render_template('signup.html', title= 'Blogz-signup', username_error="Username must be between 3 and 20 characters", username= username)

        if not passcode:
            return render_template('signup.html', title= 'Blogz-signup', password_error="Please enter password", username= username)

        if len(passcode) < 3 or len(passcode) > 20:
            return render_template('signup.html', title= 'Blogz-signup', password_error="Password must be between 3 and 20 characters", username= username)


        if not recode:
            return render_template('signup.html', title= 'Blogz-signup', re_password_error="Please re-enter password", username= username)
    
        if ' ' in passcode or ' ' in recode:
            return render_template('signup.html', title= 'Blogz-signup', password_error="Passwords have no spaces please", username= username)
        

        if recode != passcode:
            return render_template('signup.html', title= 'Blogz-signup', re_password_error="Passwords do not match", username= username)

        if len(recode) < 3 or len(recode) > 20:
            return render_template('signup.html', title= 'Blogz-signup', re_password_error="Passwords must be between 3 and 20 characters", username= username)

    
        else:
            
            existing_user = User.query.filter_by(username= username).first()
            if not existing_user:
                new_user = User(username,passcode)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
            else:
                return render_template('signup.html', title= 'Blogz-signup', username_error="username already exists")

            return redirect('/newpost')

    #else:

    return render_template('signup.html', title= 'Blogz-signup')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if session:
        del session['username']
    return redirect('/')



if __name__ == '__main__':
    app.run()
