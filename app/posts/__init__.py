from flask.blueprints import Blueprint

# collect urls of application

post_blueprint = Blueprint('posts', __name__, url_prefix='/posts')

from app.posts import views