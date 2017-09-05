from wtforms import Form, StringField, validators


class InputWordForm(Form):
    word = StringField('word', [validators.Length(min=2, max=50), validators.InputRequired()])
