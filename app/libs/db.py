import ibm_db
import time
from flask import g
from flask import current_app
from app.libs.esutil import ESUtil


class DB(object):
    def __init__(self):
        self.rule_type = current_app.config['TYPE_RULE']
        self.db2_database = current_app.config['DB2_DATABASE']
        self.db2_hostname = current_app.config['DB2_HOSTNAME']
        self.db2_port = current_app.config['DB2_PORT']
        self.db2_protocol = current_app.config['DB2_PROTOCOL']
        self.db2_uid = current_app.config['DB2_UID']
        self.db2_pwd = current_app.config['DB2_PWD']
        self.conn = ibm_db.connect("DATABASE=%s;HOSTNAME=%s;PORT=%s;PROTOCOL=%s;UID=%s;PWD=%s;" % (
        self.db2_database, self.db2_hostname, self.db2_port, self.db2_protocol, self.db2_uid, self.db2_pwd), "", "")

    def db_search(self, param):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        level = 'LEV' + '%s' % param['level']
        user = g.user.uid
        if user == 'admin':
            source = 'Atas'
        sql = "SELECT LEV10,LEV15,LEV17,LEV20,LEV30 from CMRDC.PRODUCTS_IMAGE WHERE %s = '%s'" % (
        level, param['prod_id'])
        stmt = ibm_db.exec_immediate(self.conn, sql)
        results = ibm_db.fetch_both(stmt)
        while results:
            level10 = results[0]
            level15 = results[1]
            level17 = results[2]
            level20 = results[3]
            level30 = results[4]
            results = ibm_db.fetch_both(stmt)
        try:
            insert_sql = "INSERT INTO CMRDC.LINEITEM(RLI_ID, MPP_NUMBER, VERSION, COUNTRY, DELETED, LEVEL10, LEVEL15, LEVEL17, LEVEL20, LEVEL30, SOURCE, DATE_ENTERED, DATE_MODIFIED) VALUES('%s','%s','%s','%s','%d','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            param['rli_id'], param['account_mpp'], ESUtil().rule_index, param['account_country'], param['deleted'],
            level10, level15, level17, level20, level30, source, timestamp, timestamp)
            ibm_db.exec_immediate(self.conn, insert_sql)
            ibm_db.commit(self.conn)
        except Exception as ex:
            ibm_db.rollback(self.conn)
        finally:
            ibm_db.close(self.conn)
