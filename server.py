import json
import os
import sys
from functools import wraps

import slugify as slugify
import wand.image
from flask import Flask, render_template, redirect, request, send_from_directory, current_app
from flask_admin.contrib.sqla import ModelView
from flask_babel import Babel
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import or_, and_

from data import db_session
from data.entries import Article
from data.users import User
from forms.user import LoginForm, RegisterForm
from froala_dependencies import Image, FlaskAdapter
from flask_admin import Admin, AdminIndexView

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
publicDirectory = os.path.join(BASE_DIR, "public")
if not os.path.exists(publicDirectory):
    os.makedirs(publicDirectory)

app = Flask(__name__)
app.config.from_object('config')

babel = Babel(app)


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1


admin = Admin(app, 'Admin Area', template_mode='bootstrap4', index_view=MyAdminIndexView())

login_manager = LoginManager()
login_manager.init_app(app)


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.id == 1:
            return 403
        return func(*args, **kwargs)

    return wrapper


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/', methods=["GET", "POST"])
def main_page():
    db_sess = db_session.create_session()
    result_search = db_sess.query(Article).filter(Article.is_private == 2).all()
    return render_template('main_page.html', title="Главная страница", articles=result_search)


@app.route("/public/<path:path>")
def get_public(path):
    return send_from_directory("public/", path)


@app.route("/load_images", methods=["GET", "POST"])
def load_images():
    response = Image.list("/public/images")
    return response


@app.route('/delete_image', methods=["GET", 'POST'])
def delete_image():
    src = request.data["src"]
    print(src)
    try:
        Image.delete(src)
        return "OK"
    except:
        raise Exception('Could not delete file')


@app.route("/upload_image", methods=["POST"])
def upload_image():
    try:
        response = Image.upload(FlaskAdapter(request), "/public/images/")
    except Exception:
        response = {"error": str(sys.exc_info()[1])}
    return json.dumps(response)


@app.route("/upload_image_validation", methods=["POST"])
def upload_image_validation():
    def validation(filePath, mimetype):
        with wand.image.Image(filename=filePath) as img:
            if img.width != img.height:
                return False
            return True

    options = {
        "fieldname": "myImage",
        "validation": validation
    }

    try:
        response = Image.upload(FlaskAdapter(request), "/public/images", options)
    except Exception:
        response = {"error": str(sys.exc_info()[1])}
    return json.dumps(response)


@app.route('/profile/<username>')
@login_required
def profile(username):
    if username == current_user.name:
        db_sess = db_session.create_session()
        articles = db_sess.query(Article).filter(Article.user_id == current_user.id).all()
        return render_template('profile.html', user=current_user, articles=articles)
    return redirect("/")


@app.route('/search', methods=["GET", "POST"])
def search():
    db_sess = db_session.create_session()
    result_search = None
    print("starting")
    if request.method == "POST":
        print("posted")
        query = request.form["search"]
        if query:
            print(query)
            columns = [column.key for column in Article.__table__.columns]
            column_dict_and_value = {column_name: 'value' for column_name in columns}
            condition = and_(or_(*[getattr(Article, col).ilike(f'{query}%') for col, val in column_dict_and_value.items()]),
                             Article.is_private == 2)
            # condition = or_(*[getattr(Article, col).ilike(f'{query}%') for col, val in column_dict_and_value.items()])
            result_search = db_sess.query(Article).filter(condition).all()
            return render_template('search.html', result_search=result_search)
    print("???")
    result_search = db_sess.query(Article).filter(Article.is_private == 2).all()
    return render_template('search.html', result_search=result_search)


@app.route('/create_article', methods=["GET", "POST"])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form.get('title')
        small_desc = request.form.get('small_desc')
        content = request.form.get('content')
        slug = slugify.slugify(title)
        db_sess = db_session.create_session()
        article_entry = Article(title=title, small_desc=small_desc, content=content, slug=slug, user_id=current_user.id)
        db_sess.add(article_entry)
        db_sess.commit()
        return redirect(f"/article/{slug}")
    return render_template('create_article.html', title="Создание статьи")


@app.route('/edit_article/<slug>', methods=["GET", "POST"])
@login_required
def edit_article(slug):
    db_sess = db_session.create_session()
    article_result = db_sess.query(Article).filter(Article.slug == slug).first()
    if current_user.id != article_result.user_id and current_user.id != 1:
        return redirect('/')
    if request.method == 'POST':
        title = request.form.get('title')
        small_desc = request.form.get('small_desc')
        content = request.form.get('content')
        article_result.title = title
        article_result.small_desc = small_desc
        article_result.content = content
        article_result.slug = slugify.slugify(title)
        db_sess.commit()
        return redirect(f"/article/{article_result.slug}")
    db_sess.close()
    return render_template('edit_article.html', title=article_result.title,
                           small_desc=article_result.small_desc, content=article_result.content)


@app.route('/publicate_article/<slug>', methods=["GET", "POST"])
@login_required
def publicate_article(slug):
    db_sess = db_session.create_session()
    article_result = db_sess.query(Article).filter(Article.slug == slug).first()
    if current_user.id != article_result.user_id:
        return redirect('/')
    article_result.is_private = 1
    db_sess.commit()
    return redirect('/')


@app.route('/post_article/<slug>', methods=["GET", "POST"])
@login_required
@admin_required
def post_article(slug):
    db_sess = db_session.create_session()
    article_result = db_sess.query(Article).filter(Article.slug == slug).first()
    article_result.is_private = 2
    db_sess.commit()
    return redirect('/')


@app.route("/article/<slug>")
def article(slug):
    db_sess = db_session.create_session()
    article_result = db_sess.query(Article).filter(Article.slug == slug).first()
    if article_result.is_private != 2:
        if not current_user.is_authenticated or current_user.id != article_result.user_id:
            return redirect('/')
    return render_template("article.html", article=article_result)


@app.route('/articles_browser')
@login_required
@admin_required
def articles_browser():
    db_sess = db_session.create_session()
    articles = db_sess.query(Article).filter(Article.is_private == 1).all()
    return render_template('/admin/articles_browser.html', articles=articles)


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


@app.errorhandler(401)
def page_not_found_401(e):
    return redirect('/')


@app.errorhandler(404)
def page_not_found_404(e):
    return redirect('/')


@app.errorhandler(500)
def page_not_found_500(e):
    return redirect('/')


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    admin.add_view(ModelView(User, db_sess))
    admin.add_view(ModelView(Article, db_sess))
    db_sess.close()
    app.run(port=5000, host='127.0.0.1')
