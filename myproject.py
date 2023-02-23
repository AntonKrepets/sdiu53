from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, FieldList
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()
app = Flask(__name__, template_folder='./templates')
app.config['SECRET_KEY'] = "mysupersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://test_user:test_pass@localhost:5432/test'
db.init_app(app)


class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(JSONB)
    
    def __init__(self, text):
        self.text = text      

with app.app_context():
    db.create_all()

class TextForm(FlaskForm):
    text = FieldList(StringField('input name 1'), min_entries=1)


@app.route('/', methods=['GET', 'POST'])
def index():
    textForm  = TextForm()
    if textForm.validate_on_submit():
        for i in textForm.text.entries:
            db.session.add(Text({f'input {Text.query.count() + 1}': f'{i.data}'}))
            db.session.commit()
        return render_template('submit.html', text=Text.query.all())
    return render_template('index.html', form=textForm)


if __name__ == "__main__":
    app.run(host='0.0.0.0')