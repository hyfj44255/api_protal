from app.libs.error import APIException


class Success(APIException):
    code = 201
    msg = 'ok'
    error_code = 0


class DeleteSuccess(Success):
    code = 202
    error_code = 1


class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 999


class ClientTypeError(APIException):
    # 400 request param error
    # 401 unauthed
    # 403 forbiden
    # 404
    # 500 server unknown error
    # 200 query success 201 create update success 204 delete success
    # 301 redirect 302
    code = 400
    msg = 'client is invalid'
    error_code = 1006


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class NotFound(APIException):
    code = 404
    msg = 'the resource are not found O__O...'
    error_code = 1001


class AuthFailed(APIException):
    code = 401
    error_code = 1005
    msg = 'authorization failed'


class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = 'forbidden, not in scope'


class DuplicateGift(APIException):
    code = 400
    error_code = 2001
    msg = 'the current book has already in gift'


class EmptyPayload(APIException):
    code = 400
    error_code = 2002
    msg = 'the payload is empty'


class PayloadElementsError(APIException):
    code = 400
    error_code = 2003
    msg = "the payload's parameter error"


class NoAvailableIndexError(APIException):
    code = 400
    error_code = 2004
    msg = "no available index"
