from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class QueryForm(Form):
    query = StringField('query', validators=[DataRequired()])
