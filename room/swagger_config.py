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

token_model_full = api.model('Token', {
    'id': fields.Integer,
    'token': fields.String,
    'password': fields.String,
    'creation_time': fields.String,
    '_links': fields.Nested({
        'self': fields.String,
        'update': fields.String,
        'delete': fields.String,
    })
})


# Parser for request data
token_parser = reqparse.RequestParser()
token_parser.add_argument('token', type=str, help='Token value')
token_parser.add_argument('password', type=str, help='Password associated with the token')

