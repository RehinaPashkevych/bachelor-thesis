from flask_restx import Api, fields, reqparse

api = Api(
    version='1.0',
    title='Room API',
    description='API Documentation',
)

# Model data
token_model = api.model('Token', {
    'token': fields.String(required=True, description='Token value'),
    'password': fields.String(required=False, description='Password associated with the token'),
})

# Parser for request data
token_parser = reqparse.RequestParser()
token_parser.add_argument('token', type=str, help='Token value')
token_parser.add_argument('password', type=str, help='Password associated with the token')

