from flask import render_template,request,redirect,url_for
from flask import Flask
from app.models import Post,db,Categories
import os
from werkzeug.utils import secure_filename

from app.posts import post_blueprint
from app.categories import categories_blueprint


UPLOAD_FOLDER = 'static/categories/images/'
# UPLOAD_FOLDER = 'static/posts/images/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# @app.route('/posts',endpoint='posts.index')
@categories_blueprint.route('',endpoint='index')
def category_index():
    categories = Categories.get_all_objects()
    return render_template('categories/index.html', categories=categories)

# @app.route('/posts/<int:id>',endpoint='posts.show')
@categories_blueprint.route('<int:id>',endpoint='show')
def show_category(id):
    category = Categories.query.get_or_404(id)
 
    return render_template('categories/show.html',category=category)


# create a new post

# @app.route('/create', methods=['GET', 'POST'], endpoint='create')
@categories_blueprint.route('/create', methods=['GET', 'POST'],endpoint='create')
def create():
    if request.method == 'POST':
        category = Categories(
            name=request.form['name'],
            description=request.form['description'],
        
        )

        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_image(file.filename):
                filename = secure_filename(file.filename)

                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                file.save(file_path)
                category.image = filename  # Update the post's image 
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('categories.index'))

    return render_template('categories/create.html')



ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


# edit


# @app.route('/edit/<int:id>', methods=['GET', 'POST'], endpoint='posts.edit')
@categories_blueprint.route('/edit/<int:id>',methods=['GET', 'POST'], endpoint='edit')
def edit(id):
    category = Categories.query.get(id)

    if not category:
        return "Post not found", 404

    if request.method == 'POST':
        category.name = request.form['name']
        category.description = request.form['description']

        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_image(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                category.image = filename  # Update the post's image

        db.session.commit()
        return redirect(url_for('categories.index'))

    return render_template('categories/edit.html', category=category)

# delete post
# @app.route('/posts/delete/<int:id>', endpoint='posts.delete')
@categories_blueprint.route('/delete/<int:id>', endpoint='delete')
def delete(id):
    category = Categories.query.get_or_404(id)

    # Remove the product's image file, if it exists
    if category.image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], category.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('categories.index'))