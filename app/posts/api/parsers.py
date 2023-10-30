from flask_restful import reqparse

post_request_parser = reqparse.RequestParser()

post_request_parser.add_argument("title", type=str, help='Post name is required', required=True)
post_request_parser.add_argument("image", type=str)
post_request_parser.add_argument("body", type=str)
post_request_parser.add_argument("category_id", type=int)