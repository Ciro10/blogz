from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Blog123@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    body = db.Column(db.String(500))
    

    def __init__(self, name, body):
        self.name = name
        self.body = body


@app.route('/blog', methods=['POST', 'GET'])
def index():

    name = request.args.get('id')
    if not name:
        blogs = Blog.query.all()
        return render_template('Homepage.html',title="Buid a blog", blogs=blogs)
    
    else:
        yourblog = Blog.query.filter_by(id=name).first()

        return render_template('Myblog.html', Btitle = yourblog.name, your_blog= yourblog.body)

    

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    
    if request.method == 'POST':
        
        blog_name = request.form['blog_title']
        blog_body = request.form['blog']
        
        if not blog_name:
            return render_template('Postentry.html', title_error="Please insert a title", blog= blog_body)
        if not blog_body:
            return render_template('Postentry.html', blog_error="Please insert a blog", blog_title= blog_name)
        else:

            new_blog = Blog(blog_name,blog_body)
            db.session.add(new_blog)
            db.session.commit()
 
            pin= Blog.query.filter_by(name=blog_name).first()
            
   
            return redirect('/blog?id={}'.format(pin.id))

    return render_template('Postentry.html',title="Add a Blog Entry")






if __name__ == '__main__':
    app.run()