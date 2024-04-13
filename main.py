from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from config import SECRET_KEY
from data import db_session
from data.users import User
from forms.user import LoginForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    reg_form = RegisterForm()
    log_form = LoginForm()

    if reg_form.validate_on_submit():
        if reg_form.password.data != reg_form.password_again.data:
            return render_template('main_page.html', title="Main Page", reg_form=reg_form, log_form=log_form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == reg_form.email.data).first():
            return render_template('main_page.html', title="Main Page", reg_form=reg_form, log_form=log_form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name, user.email, user.about = reg_form.name.data, reg_form.email.data, reg_form.about.data
        user.set_password(reg_form.password.data)
        db_sess.add(user)
        db_sess.commit()

    if log_form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == log_form.email.data).first()
        if user and user.check_password(log_form.password.data):
            login_user(user, remember=log_form.remember_me.data)
            return redirect("/")
        return render_template('main_page.html', title="Main Page",
                               message="Неправильный логин или пароль", reg_form=reg_form, log_form=log_form)
    return render_template('main_page.html', title="Main Page", reg_form=reg_form, log_form=log_form)


@app.route('/profile/<username>')
@login_required
def profile(username):
    if username == current_user.name:
        return render_template('profile.html', user=current_user)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=5000, host='127.0.0.1')
