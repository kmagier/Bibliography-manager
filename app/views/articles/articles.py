from flask import Blueprint, render_template, request, current_app, jsonify
from models.user import User
from models.article import Article
from database import db
import string, random
from flask_login import login_required

articles_bp = Blueprint('articles', __name__, static_folder='static')
DIR_PATH = 'static/files/'


@articles_bp.route('/add', methods=['POST', 'GET'])
@login_required
def add_article():
    u = User.query.get(1)
    if request.method == 'POST':
        author = request.form.get('Author')
        title = request.form.get('Title')
        pages = request.form.get('Pages')
        pdfile = request.files['Article']
        if(len(pdfile.filename) > 0):
            filename_prefix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            new_filename = filename_prefix + pdfile.filename
            path_to_file = DIR_PATH + new_filename
            pdfile.save(path_to_file)
            article = Article(author=author, title=title, pages=pages, file_path=path_to_file, owner=u)
            db.session.add(article)
            db.session.commit()
            current_app.logger.debug('Uploaded article - Author:{}, Title:{}, Pages{}, File{}'.format(author, title, pages, path_to_file))
        else:
            current_app.logger.debug('Failed to upload file') 
    return render_template("add-article.html")

@articles_bp.route('/list', methods=['GET'])
def show_articles():
    u = User.query.get(1)
    _articles = u.articles.all()
    articleList = []
    for article in _articles:
        articleList.append(article.title)
    return jsonify(articleList)