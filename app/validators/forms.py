import time

from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp
from wtforms import ValidationError

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import EmptyPayload, PayloadElementsError
from app.models.user import User
from app.validators.base import BaseForm as Form


class ClientForm(Form):
    account = StringField(validators=[DataRequired(message='can not be null'), length(
        min=5, max=32
    )])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    nickname = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()


class BookSearchForm(Form):
    q = StringField(validators=[DataRequired()])


class TokenForm(Form):
    token = StringField(validators=[DataRequired()])


class EsQueryForm(Form):
    payload = StringField(validators=[DataRequired()])
    timestamp = StringField(validators=[DataRequired()])

    def validate_payload(self, value):
        keys = ["rli_id", "account_mpp", "account_country", "prod_id", "prod_level"]
        if isinstance(value.data, list):
            for elements in value.data:
                for x in elements:
                    if x not in keys or not is_element_valid(elements[x]):
                        if x == 'account_country':
                            pass
                        else:
                            raise PayloadElementsError()
        else:
            raise EmptyPayload()

    def validate_timestamp(self, value):
        try:
            time.mktime(time.strptime(value.data, "%Y-%m-%d %H:%M:%S.%f"))
        except Exception as e:
            raise e
        # self.type.data = client


def is_element_valid(obj):
    if isinstance(obj, str):
        if len(obj.strip()) == 0:
            return False
    elif isinstance(obj, int):
        return True
    return True
