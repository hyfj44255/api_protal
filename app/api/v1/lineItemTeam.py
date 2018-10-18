import time
from app.libs.esutil import ESUtil, query_statement_or
from app.libs.redprint import Redprint
from app.models.lit import LIT
from app.validators.forms import EsQueryForm
from app.libs.token_auth import auth
from flask import jsonify

api = Redprint('lineItemTeam')


@api.route('/', methods=['POST'])
@auth.login_required
def create_client():
    form = EsQueryForm().validate_for_api()
    payload = form.payload.data
    timestamp = form.timestamp.data
    bean_list = []
    for param in payload:
        country = param['account_country']
        country = country if len(country.strip()) != 0 else 'WW'
        account = param['account_mpp'] + country
        product = param['prod_id']
        product_level = "product_" + str(param['prod_level'])
        query = "query_statement_or(account=account, " + product_level + "=product)"
        query = eval(query)
        user_list = ESUtil().es_search(query, "rules")
        userlist = []
        for doc in user_list:
            userlist.append(doc["_source"]["user"])
        if len(userlist) == 0:
            status_code = 0
            status_info = "No users exist"
        else:
            status_info = "Find users successfully"
            status_code = 1
        bean = LIT(ESUtil().rule_index, param["rli_id"], param['account_mpp'], param['account_country'],
                   param['prod_id'], status_code, status_info, userlist)
        bean_list.append(dict(bean))
    current_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    box = dict(payload=bean_list, timestamp=current_timestamp)
    return jsonify(box)
