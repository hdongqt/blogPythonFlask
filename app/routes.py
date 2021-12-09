import os
import secrets
from flask import render_template,url_for, redirect,flash,request,abort
from flask import redirect
from app import app,db,bcrypt
from app.forms import RegistrationForm, LoginForm,UpdateAccountForm,PostForm
from app.models import User,Post
from flask_login import login_user, current_user, logout_user, login_required


# session['featured'] = Post.query.all()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html')

def getFeatured():
    return Post.query.limit(3).all()

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('list_post.html', posts=posts,featured=getFeatured())




@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        check = User.query.filter((User.username == form.username.data) | (User.email == form.email.data ))
        if(check.first() != None ):
            flash('Tài khoản đã tồn tại !', 'danger')
            return redirect(url_for('register'))
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,fullname=form.fullname.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Tạo mới tài khoản thành công , hãy đăng nhập !', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Đăng ký', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Thông tin đăng nhập sai, hãy thử lại !', 'danger')
    return render_template('login.html', title='Đăng nhập', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.fullname = form.fullname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Tài khoản đã được cập nhật thành công !', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.fullname.data = current_user.fullname
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = None
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            post = Post(title=form.title.data,image_post = picture_file ,content=form.content.data, author=current_user)
        else:
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Tạo mới bài viết thành công !', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')



@app.route("/post/manager")
@login_required
def manager_post():
    # user_id = c
    posts =  current_user.posts
    return render_template('manager_post.html', posts=posts)




@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post,featured=getFeatured())


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            post.image_post = picture_file
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Cập nhật bài viết thành công!', 'success')
        return redirect(url_for('manager_post'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.picture.data = post.image_post
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post',image_file=post.image_post)


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Đã xoá bài viết !', 'success')
    return redirect(url_for('manager_post'))