from flask_restful import reqparse, abort


def check_auth(key):
    if key != 'dev':
        raise Warning('Invalid token')

def authenticate(func):
    def wrapper(*args, **kwargs):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('key', type=str, required=True)
            check_auth(parser.parse_args()['key'])
            return func(*args, **kwargs)
        except Warning:
            abort(401, message='Auth token missing or invalid')


    return wrapper