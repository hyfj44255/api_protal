import threading
import os

from elasticsearch import Elasticsearch
from flask import current_app
from elasticsearch.helpers import scan


class ESUtil(object):
    """docstring for ESUtil"""
    __instance_lock = threading.Lock()

    ES = None
    es_host = None
    es_port = None
    es_scheme = None
    es_secret = None
    es_account = None
    rule_index = None
    rule_type = None
    login_index = None
    login_type = None
    version_index = None
    version_type = None

    def __new__(cls, *args, **kwargs):
        # the core of singleton thread safe
        if not hasattr(ESUtil, "_instance"):
            with ESUtil.__instance_lock:
                if not hasattr(ESUtil, "_instance"):
                    ESUtil._instance = object.__new__(cls)
                    ESUtil._instance.__init_es()
        return ESUtil._instance

    def __init__(self):
        super(ESUtil, self).__init__()

    def __init_es(self):
        self.es_host = setting_from_env('ES_HOST')
        self.es_port = setting_from_env('ES_PORT')
        self.es_scheme = setting_from_env('ES_HTTP_SCHEME')
        self.es_secret = setting_from_env('ES_HTTP_AUTH_SECRET')
        self.es_account = setting_from_env('ES_HTTP_AUTH_ACCOUNT')

        # self.rule_index = setting_from_env('INDEX_RULE')
        self.rule_type = setting_from_env('TYPE_RULE')

        self.login_index = setting_from_env('INDEX_SECRET')
        self.login_type = setting_from_env('TYPE_SECRET')
        self.version_type = setting_from_env('VERSION_TYPE')
        self.version_index = setting_from_env('VERSION_INDEX')
        self.ES = Elasticsearch([dict(host=self.es_host, port=self.es_port)], send_get_body_as='POST')

    def es_search(self, query, action):
        """
        query = {"query": {"bool": {"should": [{"match": {"account": account}}, {"match": {"prod": prod}}, ]}}}
        """
        all_doc = None
        userlist = []
        if action == 'secret':
            all_doc = self.ES.search(index=self.login_index, doc_type=self.login_type, body=query)
            return all_doc
        elif action == 'rules':
            target_index = self.change_index_ver()
            if target_index:
                self.rule_index = target_index
                all_doc = scan(self.ES, index=self.rule_index, doc_type=self.rule_type, query=query)
                # all_doc = self.ES.search(index=self.rule_index, doc_type=self.rule_type, body=query)
                for doc in all_doc:
                    userlist.append(doc)
                return userlist

    def change_index_ver(self):
        query = query_statement(True, version="current")
        hits = self.ES.search(index=self.version_index, doc_type=self.version_type, body=query)
        doc = hits['hits']['hits']
        count = hits['hits']['total']
        if count == 1:
            doc = hits['hits']['hits']
            for element in doc:
                source = element["_source"]
                return source["name"]
        else:
            return None


def query_statement(strong, **cols):
    match_list = []
    for elements in cols:
        match_list.append(dict(match={elements: cols[elements]}))
    way = dict(must=match_list)
    score = dict(bool=way)
    query = dict(query=score)
    return query


def setting_from_env(key):
    val = None
    try:
        val = os.environ[key]
    except Exception as e:
        return current_app.config[key]
    else:
        return val


def query_statement_or(**cols):
    also = {}  # and
    also2 = {}
    and_List = []
    for elements in cols:
        and_List.append(dict(match={elements: cols[elements]}))

    block1 = dict(must=and_List)
    count = 0
    and_List2 = []
    for elements in cols:
        if count == 0:
            count = count + 1
            and_List2.append(dict(match={elements: cols[elements]}))
        else:
            and_List2.append(dict(match={elements: "ALL"}))

    block2 = dict(must=and_List2)

    also['bool'] = block1
    also2['bool'] = block2

    ei_or = []  # or
    ei_or.append(also)
    ei_or.append(also2)

    query = dict(query=dict(bool={"should": ei_or}))
    return query
