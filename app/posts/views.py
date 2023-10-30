from flask import render_template,request,redirect,url_for
from flask import Flask
from app.models import Post,db,Categories
import os
from werkzeug.utils import secure_filename

from app.posts import post_blueprint


# UPLOAD_FOLDER = 'static/posts/images/'

app = Flask(__name__)


app_directory = 'app'

# Specify the path for the upload folder inside the 'app' directory
UPLOAD_FOLDER = os.path.join(app_directory, 'static', 'posts', 'images')

# Set the UPLOAD_FOLDER in your app's configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the 'static/posts/images' directory if it doesn't exist within the 'app' directory
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



# app_directory = 'app'

# # Specify the path for the 'static/posts/images' directory
# UPLOAD_FOLDER_POSTS = os.path.join(app_directory, 'static', 'posts', 'images')

# # Specify the path for the 'static/categories/images' directory
# UPLOAD_FOLDER_CATEGORIES = os.path.join(app_directory, 'static', 'categories', 'images')

# # Set the UPLOAD_FOLDER for 'static/posts/images' in your app's configuration
# app.config['UPLOAD_FOLDER_POSTS'] = UPLOAD_FOLDER_POSTS

# # Set the UPLOAD_FOLDER for 'static/categories/images' in your app's configuration
# app.config['UPLOAD_FOLDER_CATEGORIES'] = UPLOAD_FOLDER_CATEGORIES

# # Create the 'static/posts/images' directory if it doesn't exist within the 'app' directory
# if not os.path.exists(UPLOAD_FOLDER_POSTS):
#     os.makedirs(UPLOAD_FOLDER_POSTS)

# # Create the 'static/categories/images' directory if it doesn't exist within the 'app' directory
# if not os.path.exists(UPLOAD_FOLDER_CATEGORIES):
#     os.makedirs(UPLOAD_FOLDER_CATEGORIES)











# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
# @app.route('/posts',endpoint='posts.index')
@post_blueprint.route('',endpoint='index')
def post_index():
    posts=Post.get_all_posts()
    return render_template('posts/index.html', posts=posts)

# @app.route('/posts/<int:id>',endpoint='posts.show')
@post_blueprint.route('<int:id>',endpoint='show')
def show_post(id):
    post=Post.get_speacific_post(id)
    # post=Post.query.get_or_404(id)

    return render_template('posts/show.html',post=post)


# create a new post

# @app.route('/create', methods=['GET', 'POST'], endpoint='create')
@post_blueprint.route('/create', methods=['GET', 'POST'],endpoint='create')
def create():
    categories =Categories.get_all_objects()
    if request.method == 'POST':
        post = Post(
            title=request.form['title'],
            body=request.form['body'],
            category_id=request.form['category_id']
        
        )

        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_image(file.filename):
                filename = secure_filename(file.filename)

                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                file.save(file_path)
                post.image = filename  # Update the post's image 
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.index'))

    return render_template('posts/create.html',categories=categories)



ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


# edit


# @app.route('/edit/<int:id>', methods=['GET', 'POST'], endpoint='posts.edit')
@post_blueprint.route('/edit/<int:id>',methods=['GET', 'POST'], endpoint='edit')
def edit(id):
    post = Post.query.get(id)

    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        post.title = request.form['title']
        post.body = request.form['body']

        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_image(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                post.image = filename  # Update the post's image

        db.session.commit()
        return redirect(url_for('posts.index'))

    return render_template('posts/edit.html', post=post)

# delete post
# @app.route('/posts/delete/<int:id>', endpoint='posts.delete')
@post_blueprint.route('/delete/<int:id>', endpoint='delete')
def delete(id):
    post = Post.query.get_or_404(id)

    # Remove the product's image file, if it exists
    if post.image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], post.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts.index'))