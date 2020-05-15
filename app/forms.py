from datetime import datetime

from flask_wtf import FlaskForm
import wtforms as form
from wtforms import validators as v
from wtforms_json import init

# Allow wtforms to work with JSON
init()


class DefaultUserForm(FlaskForm):
    user_id = form.IntegerField(validators=[v.DataRequired()])


class Future(object):
    """ Checks if date gather than `now` """
    def __call__(self, form, field):
        td = datetime.now()
        return field.data > td


class Past(object):
    def __call__(self, form, field):
        td = datetime.now()
        return field.data < td


class ListForm(DefaultUserForm):
    page_token = form.StringField()

    class Meta:
        csrf = False


class PostForm(FlaskForm):
    user_ids = form.FieldList(form.IntegerField(), validators=[v.DataRequired()])
    message = form.StringField(validators=[v.InputRequired()])
    img_url = form.StringField(validators=[v.Optional(), v.URL()])
    expire = form.IntegerField(validators=[v.optional(), v.NumberRange(min=0)])
    lesson_id = form.IntegerField(validators=[v.Optional()])
    show_at = form.DateTimeField(validators=[v.Optional(), Future()], format='%d.%m.%Y %H:%M')

    class Meta:
        csrf = False