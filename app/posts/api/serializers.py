from flask_restful import  fields


category_serializer={
    "id":fields.Integer,
    "name":fields.String,
}


post_serializer={
    "id":fields.Integer,
    "title":fields.String,
    'body':fields.String,
    "image":fields.String,
    "created_at":fields.DateTime,
    "updated_at":fields.DateTime,
    'category_id':fields.Integer,
    'category':fields.Nested(category_serializer)
    }