from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate, MigrateCommand
from flask_moment import Moment
from flask_script import Manager, Shell
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:wt0330321@my.blueness.net:33306/flasky'
app.config['SQLALCHEY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)

    users = db.relationship('User', backref = 'role', lazy = "dynamic")

    def __repr__(self):
        return '<Role %r>' %self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators = [DataRequired()])
    submit = SubmitField('Submit')

def make_shell_context():
    return dict(db = db, User = User, Role = Role, aaa= 'bbb')

manager.add_command("shell", Shell(make_context = make_shell_context))
manager.add_command('db', MigrateCommand)

@app.route('/', methods = ['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           form = form,
                           name = session.get('name'),
                           konwn = session.get('known', False))

if __name__ == '__main__':
    # app.run()
    manager.run()