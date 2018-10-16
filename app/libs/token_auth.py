import hashlib
from collections import namedtuple

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth, HTTPDigestAuth
from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer, BadSignature, SignatureExpired

from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope
from app.libs.esutil import query_statement, ESUtil

auth = HTTPBasicAuth()
User = namedtuple('User', ['uid'])


@auth.verify_password
def verify_password(account, password):
    # token
    # HTTP 账号密码
    # header key:value
    # key=Authorization
    # value =basic base64(qiyue:123456)
    user_info = verify_account_secret(account, password)
    if not user_info:
        return False
    else:
        # g variable is similar 2 request obj
        g.user = user_info
        return True


def verify_account_secret(account, password):
    pwd_md5 = hashlib.md5(password.encode(encoding='utf-8')).hexdigest()
    query = query_statement(True, account=account, password=pwd_md5, active=1)
    res = ESUtil().es_search(query, "secret")
    if res:
        doc_res = res['hits']
        res_count = doc_res["total"]
        if res_count == 1:
            return User(account)
        else:
            raise Forbidden()
    else:
        raise Forbidden()


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)  # 解密
    except BadSignature:  # 合法?
        raise AuthFailed(msg='token is invalid',
                         error_code=1002)
    except SignatureExpired:  # 过期
        raise AuthFailed(msg='token is expired',
                         error_code=1003)
    uid = data['uid']
    ac_type = data['type']
    scope = data['scope']
    # request 视图函数
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    return User(uid, ac_type, scope)
