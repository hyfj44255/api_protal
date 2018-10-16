class LIT(object):

    def __init__(self, index_version, rli_id, account_mpp, account_country, prod_id, status_code, status_info, user_cnum):
        super(LIT, self).__init__()
        self.rli_id = rli_id
        self.account_mpp = account_mpp
        self.account_country = account_country
        self.prod_id = prod_id
        self.user_cnum = user_cnum
        self.status_code = status_code
        self.status_info = status_info
        self.index_version = index_version

    def keys(self):
        return ['index_version', 'account_mpp', 'account_country', 'prod_id','rli_id', 'status_code',
                'status_info', 'user_cnum']

    def __getitem__(self, item):
        return getattr(self, item)