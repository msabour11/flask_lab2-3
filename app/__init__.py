from flask import Flask
from flask import render_template
# load configuration
from app.config import projectConfig as AppConfig
from app.models import db
# from app.posts.views import post_index,show_post,create,edit,delete
from app.posts import post_blueprint
from app.categories import categories_blueprint
from flask_migrate import Migrate
from flask_restful import Resource, Api
from app.posts.api.api_views import PostListClass,PostResource

def create_app(config_name='prd'):
    app= Flask(__name__)
    current_App_Config = AppConfig[config_name]
    # current_App_Config = AppConfig[config_name]
    app.config["SQLALCHEMY_DATABASE_URI"] = current_App_Config.SQLALCHEMY_DATABASE_URI
    app.config.from_object(current_App_Config)
    db.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)

    api.add_resource( PostListClass,'/api/posts/')
    api.add_resource(PostResource, '/api/posts/<int:post_id>')

    #assign routes 

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('notfound.html')
    

    app.register_blueprint(post_blueprint)
    app.register_blueprint(categories_blueprint)



    return app