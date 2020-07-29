from flask import Blueprint, render_template, request, current_app
from models.user import User
from models.article import Article
from database import db
from flask_login import login_required, current_user

articles_bp = Blueprint('articles', __name__, static_folder='static')
DIR_PATH = 'static/files/'


@articles_bp.route('/add-article', methods=['POST', 'GET'])
@login_required
def add_article():
    user = current_user
    return render_template("add-article.html")

@articles_bp.route('/article-list', methods=['GET'])
@login_required
def show_articles():
    user = current_user
    articles = user.articles.all()
    if not articles:
        hasArticles = False
    else:
        hasArticles = True
    return render_template('article-list.html', hasArticles = hasArticles)
    
