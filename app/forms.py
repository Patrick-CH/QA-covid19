from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Email, URL


class AskForm(FlaskForm):
    question = StringField('请输入您的问题', validators=[DataRequired()])
    submit = SubmitField("提问", render_kw={"class": "submit_btn"})