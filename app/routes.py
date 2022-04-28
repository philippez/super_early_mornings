from flask import render_template, flash, redirect, url_for, request
import pandas as pd
from sqlalchemy import func
from datetime import date, datetime
from werkzeug.urls import url_parse
from app import app, db
from app.forms import AssetPriceForm, LoginForm, RegistrationForm, EditProfileForm, RegisterAssetForm, RegisterSuperThemeForm, PostForm, EmptyForm, TestForm, RegisterPlatformForm, RegisterTransactionForm, RegisterTxTypeForm, AssetPriceForm
from flask_login import current_user, login_required, login_user, logout_user
from app.models import Asset_Prices, User, Asset, Super_Theme, Post, Opinion, Platform, Transaction, Tx_Type, Asset_Prices

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/register_asset', methods=['GET', 'POST'])
def register_asset():
    available_super_themes = db.session.query(Super_Theme).all()
    super_themes_list = [(i.id, i.super_theme_name) for i in available_super_themes]
    form = RegisterAssetForm()
    form.super_theme.choices = super_themes_list
    if form.validate_on_submit():
        asset = Asset(
            timestamp=datetime.utcnow(),
            asset_name=form.asset_name.data, 
            asset_desc=form.asset_desc.data,
            asset_currency=form.asset_currency.data,
            asset_region=form.asset_region.data,
            asset_type=form.asset_type.data,
            super_theme=form.super_theme.data,
            micro_theme=form.micro_theme.data,
            bloomberg_ticker=form.bloomberg_ticker.data,
            sec_ref=form.sec_ref.data,
            user_id = current_user.id
            )
        db.session.add(asset)
        db.session.commit()
        flash('Congratulations, you have created an asset!')
        return redirect(url_for('index'))
    return render_template('admin/register_asset.html', title='Register Asset', form=form)

@app.route('/register_super_theme', methods=['GET', 'POST'])
def register_super_theme():
    form = RegisterSuperThemeForm()
    if form.validate_on_submit():
        super_theme = Super_Theme(
            timestamp=datetime.utcnow(),
            super_theme_name=form.super_theme_name.data, 
            super_theme_desc=form.super_theme_desc.data)        
        db.session.add(super_theme)
        db.session.commit()
        flash('Congratulations, you have created a super theme!')
        return redirect(url_for('register_super_theme'))
    return render_template('admin/register_super_theme.html', title='Register Super Theme', form=form)


@app.route('/register_platform', methods=['GET', 'POST'])
def register_platform():
    form = RegisterPlatformForm()
    if form.validate_on_submit():
        platform = Platform(
            platform_name=form.platform_name.data, 
            platform_desc=form.platform_desc.data)        
        db.session.add(platform)
        db.session.commit()
        flash('Congratulations, you have created a platform!')
        return redirect(url_for('register_platform'))
    return render_template('admin/register_platform.html', title='Register Platform', form=form)

@app.route('/register_tx_type', methods=['GET', 'POST'])
def register_tx_type():
    form = RegisterTxTypeForm()
    if form.validate_on_submit():
        tx_type = Tx_Type(
            tx_type_name=form.tx_type_name.data, 
            tx_type_desc=form.tx_type_desc.data)        
        db.session.add(tx_type)
        db.session.commit()
        flash('Congratulations, you have created a transaction type!')
        return redirect(url_for('register_tx_type'))
    return render_template('admin/register_tx_type.html', title='Register Transaction Type', form=form)

@app.route('/register_transaction', methods=['GET', 'POST'])
def register_transaction():

    available_tx_types = db.session.query(Tx_Type).all()
    tx_types_list = [(i.id, i.tx_type_name) for i in available_tx_types]

    available_assets = db.session.query(Asset).all()
    assets_list = [(i.id, i.asset_name) for i in available_assets]

    available_platforms = db.session.query(Platform).all()
    platforms_list = [(i.id, i.platform_name) for i in available_platforms]
  
    form = RegisterTransactionForm()
    form.transaction_asset.choices = assets_list
    form.transaction_platform.choices = platforms_list
    form.transaction_type.choices = tx_types_list
    
    if form.validate_on_submit():
        transaction = Transaction(
            date=form.transaction_date.data,
            type=form.transaction_type.data,
            qty=form.transaction_qty.data,
            price=form.transaction_price.data,
            asset_id=form.transaction_asset.data,
            platform_id=form.transaction_platform.data)        
        db.session.add(transaction)
        db.session.commit()
        flash('Congratulations, you have created a transaction!')
        return redirect(url_for('register_transaction'))
    return render_template('admin/register_transaction.html', title='Register Transaction', form=form)

@app.route('/view_assets')
def view_assets():
    assets = Asset.query.all()
    return render_template('view_assets.html', assets = assets)

@app.route('/view_super_themes')
def view_super_themes():
    super_themes = Super_Theme.query.all()
    return render_template('view_super_themes.html', super_themes = super_themes)

@app.route('/view_transactions')
def view_transactions():
    q = db.session.query(Transaction, Platform, Asset)
    res = q.filter(Transaction.asset_id == Asset.id).filter(Transaction.platform_id == Platform.id)
    return render_template('view_transactions.html', res = res)


@app.route('/view_manual_prices')
def view_manual_prices():
    q = db.session.query(Asset_Prices, Asset)
    res = q.filter(Asset_Prices.asset_id == Asset.id)
    return render_template('view_manual_prices.html', res = res)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html", title='Explore', posts=posts.items,
                            next_url=next_url, prev_url=prev_url)

@app.route('/admin')
def admin():
    if current_user.username != 'Phil':
        return "Access forbidden"
    else:
        return render_template('admin.html')

@app.route('/user/<username>/investor_profile')
@login_required
def investor_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = TestForm()
    return render_template("investor_profile.html", title='Investor profile', user=user)


@app.route('/user/<username>/test_form')
@login_required
def test_form(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = TestForm()
    return render_template("test_form.html", title='Test Form', form=form, user=user)


@app.route('/portfolio_performance')
def portfolio_performance():
    base_query = db.session.query(Transaction).join(Asset, Transaction.asset_id == Asset.id).add_columns(Transaction.date, Transaction.qty,Transaction.price, Asset.asset_name).all()

    other_query = db.session.query(Transaction, func.sum(Transaction.qty * Transaction.price).label('Total_cost')).join(Asset, Transaction.asset_id == Asset.id).group_by(Asset.asset_name).add_columns(Asset.asset_name).all()


    print(str(base_query))
    print(str(other_query))


    return render_template('portfolio_performance.html', res=base_query, res_2=other_query)

@app.route('/manual_prices', methods=['GET', 'POST'])
def manual_prices():
    print("function started")
    available_assets = db.session.query(Asset).all()
    print("avail assets")
    assets_list = [(i.id, i.asset_name) for i in available_assets]    
    print("assets list")
    form = AssetPriceForm()
    print("form")
    form.asset.choices = assets_list
    print("choices")

    if form.validate_on_submit():
        print("validated")
        asset_price = Asset_Prices(
            date=form.date.data, 
            asset_id=form.asset.data,
            price=form.price.data
            )
        print("asset price created")
        db.session.add(asset_price)
        db.session.commit()
        flash('Congratulations, you have created an asset price!')
        return redirect(url_for('manual_prices'))

    return render_template('admin/register_asset_price.html', form=form)


# @app.route('/manual_prices')
# def manual_prices():

#     available_assets = db.session.query(Asset_Prices).all()
#     assets_list = [(i.id, i.asset) for i in available_assets]    

#     form = AssetPriceForm()
#     form.asset.choices = assets_list

#     return render_template('admin/register_asset_price.html', form=form)


