"""
 entrance file
"""
from werkzeug.exceptions import HTTPException
from app import create_app
from app.libs.error import APIException
from app.libs.error_code import ServerError

app = create_app()

"""
AOP get all kinds of exception
"""


@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # debug mode
        # log
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
    # , debug=True
    # , ssl_context = (
    #     "C:/https/server/server-cert.pem",
    #     "C:/https/server/server-key.pem")
