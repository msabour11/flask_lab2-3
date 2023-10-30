from flask_sqlalchemy import SQLAlchemy
from flask import  url_for

db = SQLAlchemy()

# models 
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    image = db.Column(db.String,nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_onupdate=db.func.now(), server_default=db.func.now())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    # category = db.relationship('Categories', backref='posts_list')

    def __str__(self):
        return f'{self.title}'
    
    @classmethod
    def get_all_posts(cls):
        return cls.query.all()
    @classmethod
    def get_speacific_post(cls,id):
        return cls.query.get_or_404(id)
    

    @property
    def show_url(self):
        return url_for('posts.show', id=self.id)
    


    @classmethod
    def save_object(cls, requestdata):
        std = cls(**requestdata)
        db.session.add(std)
        db.session.commit()
        return std
    

    @classmethod
    def delete_object(cls, id):
        post = cls.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        return True












class Categories(db.Model):
    __tablename__='categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    image = db.Column(db.String,nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime,server_onupdate=db.func.now(), server_default=db.func.now())
    posts = db.relationship('Post', backref='category')


    def __str__(self):
        return f"{self.name}"
    @classmethod
    def get_all_objects(cls):
        return  cls.query.all()

    @classmethod
    def save_category(cls, request_data):
        category  =cls(**request_data)
        db.session.add(category)
        db.session.commit()
        return category
    
    @property
    def show_url(self):
        return url_for('categories.show', id=self.id)
