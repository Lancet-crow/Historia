from flask import Flask, render_template, redirect, request
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
    return db_sess.get(User, user_id)


@app.route('/')
def main_page():
    return render_template('main_page.html', title="Main Page")


@app.route('/profile/<username>')
@login_required
def profile(username):
    if username == current_user.name:
        return render_template('profile.html', user=current_user)
    return redirect("/")


@app.route('/test_page')
def test_page():
    return render_template('create_article.html', title="TEST Page")


@app.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegisterForm()
    referrer = request.args.get('redirected_from')
    referrer = "/" if not referrer else referrer
    if reg_form.validate_on_submit():
        if reg_form.password.data != reg_form.password_again.data:
            return render_template('register.html', title="Register Page", reg_form=reg_form,
                                   register_message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == reg_form.email.data).first():
            return render_template('register.html', title="Register Page", reg_form=reg_form,
                                   register_message="Такой пользователь уже есть")
        if reg_form.form_errors:
            return render_template('register.html', title="Register Page", reg_form=reg_form,
                                   register_message="Допущена ошибка в данных")
        user = User()
        user.name, user.email, user.about = reg_form.name.data, reg_form.email.data, reg_form.about.data
        user.set_password(reg_form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login?redirected_from=" + referrer)
    return render_template('register.html', title="Register Page", reg_form=reg_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    log_form = LoginForm()
    referrer = request.args.get('redirected_from')
    referrer = "/" if not referrer else referrer
    if log_form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == log_form.email.data).first()
        if user and user.check_password(log_form.password.data):
            login_user(user, remember=log_form.remember_me.data)
            return redirect(referrer)
        return render_template('login.html', title="Login Page", log_form=log_form,
                               login_message="Неправильный логин или пароль")
    return render_template('login.html', title="Login Page", log_form=log_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=5000, host='127.0.0.1')
