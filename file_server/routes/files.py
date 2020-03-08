from flask import Flask, Blueprint, render_template, request, current_app, redirect, url_for, jsonify, send_file
from models.article import Article
from models.user import User
from database import db
from flask_login import login_required, logout_user, current_user, login_user
import bcrypt
import sys
import string, random
from flask_cors import CORS, cross_origin

files_bp = Blueprint('files', __name__)
DIR_PATH = 'static/files/'
CORS(files_bp)

@files_bp.route('/article-list', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@cross_origin(supports_credentials=True, origins=['https://localhost:8080'])
def get_articles():
    user = current_user
    articleList = []  
    if user.is_anonymous == False:
        _articles = user.articles.all()
        for article in _articles:
            articleList.append(article.serialize())
        response = jsonify(articleList)
    else:
        response = jsonify('No files or user logged out.')
        current_app.logger.debug('User logged out or not found')
    return response

@files_bp.route('/article-list/files/<string:article_name>', methods=['GET'])
def download_article(article_name):
    article = Article.query.filter_by(article_hash=article_name).first()
    if article is not None:
        path_to_file = article.file_path
        org_filename = article.org_filename
        try:
            return send_file(path_to_file, attachment_filename = org_filename, as_attachment = True)
        except Exception as e:
            print(e, file = sys.stderr)
    return path_to_file, 200


@files_bp.route('/add-article', methods=['POST', 'OPTIONS'])
@login_required
@cross_origin(supports_credentials=True, origins=['https://localhost:8080'])
def add_article():
    user = current_user
    if request.method == 'POST':
        author = request.form.get('Author')
        title = request.form.get('Title')
        pages = request.form.get('Pages')
        pdfile = request.files['Article']
        if(len(pdfile.filename) > 0):
            filename_prefix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            new_filename = filename_prefix + '.' + pdfile.filename.split('.')[-1]
            path_to_file = DIR_PATH + new_filename
            pdfile.save(path_to_file)
            article = Article(author=author, title=title, pages=pages, file_path=path_to_file, 
                            org_filename=pdfile.filename, article_hash=new_filename, owner_id=user.id)
            db.session.add(article)
            db.session.commit()
            response = jsonify('Success, file received.')
            current_app.logger.debug('Uploaded article - Author:{}, Title:{}, Pages{}, File{}'.format(author, title, pages, path_to_file))
        else:
            current_app.logger.debug('Failed to upload file') 
            response = jsonify('Failed to receive file.')
    else:
        response = jsonify('Wrong request type.')
    return response