from flask import Blueprint, render_template, request, current_app, jsonify, send_file
from models.user import User
from models.article import Article
from database import db
import string, random
from flask_login import login_required, current_user
import os, sys

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
    current_app.logger.debug("Articles: {}".format(articles))
    if not articles:
        hasArticles = False
    else:
        hasArticles = True
    return render_template('article-list.html', hasArticles = hasArticles)
    

# @articles_bp.route('/articles', methods=['GET'])
# def get_data():
#     user = current_user
#     articles = user.articles.all()
#     articleList = []
#     for article in articles:
#         articleList.append(article.serialize())
#     return jsonify(articleList)

# @articles_bp.route('/article-list/<int:article_id>', methods=["GET"])
# def download_article(article_id):
#     user=current_user
#     article = user.articles.filter_by(id=article_id).first()
#     if article is not None:
#         try:
#             return send_file(article.file_path, attachment_filename=article.org_filename, as_attachment=True)
#         except Exception as e:
#             print(e, file = sys.stderr)
#     return article.file_path
