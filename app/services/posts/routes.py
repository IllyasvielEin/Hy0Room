from flask import Blueprint, session, request, render_template, redirect, url_for, current_app, flash, jsonify

from app.hyldb.handler.reports import ReportsHandler
from app.hyldb.handler.users import UserHandler, Users
from app.hyldb.handler.posts import PostsHandler, PostState
from app.hyldb.models.reports import ReportType
from app.utils.generate_template import get_markup

post_bp = Blueprint('post', __name__, url_prefix='/post')


@post_bp.before_request
def require_login():
    if 'user_id' not in session:
        return redirect(url_for('main.index'))

@post_bp.route('/add', methods=['POST'])
def create_post():

    user_id = session['user_id']
    title = request.form.get('post_title')
    content = request.form.get('post_content')

    if PostsHandler.add_post(user_id=user_id, title=title, content=content):
        flash(
            get_markup(
                show_message="Add post success"
            ), 'success'
        )
    else:
        flash(
            get_markup(
                show_message="Add post error, please try later"
            ), 'danger'
        )

    return redirect(url_for('main.index', active_label=2))

@post_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id: int):
    post = PostsHandler.get_one_post(post_id)
    if post.parent_id is not None:
        return render_template(url_for('main.index', active_label=2))
    return render_template(
        'post.html',
        post=post
    )

@post_bp.route('/<int:origin_post>/delete/<int:post_id>', methods=['GET'])
def delete_post(origin_post: int, post_id: int):
    # current_app.logger.info(f"delete {post_id}")

    if PostsHandler.delete_post(post_id=post_id):
        flash(
            get_markup(
                show_message="Delete post success"
            ), 'success'
        )
    else:
        flash(
            get_markup(
                show_message="Delete post error, please try later"
            ), 'danger'
        )
    if origin_post == post_id:
        return redirect(url_for('main.index', active_label=2))
    return redirect(url_for('post.get_post', post_id=origin_post))


@post_bp.route('/edit', methods=['POST'])
def edit_post():
    post_id = request.args.get('post_id')
    current_app.logger.info(f"edit {post_id}")

    return redirect(url_for('main.index', active_label=2))


@post_bp.route('/<int:post_id>/comment', methods=['POST'])
def comment_post(post_id: int):
    user_id = session['user_id']
    parent_id = request.form.get('parent_id')
    title = request.form.get('post_title')
    content = request.form.get('post_content')

    if PostsHandler.add_post(user_id=user_id, title=title, content=content, parent_id=parent_id):
        flash(
            get_markup(
                show_message="Add post success"
            ), 'success'
        )
    else:
        flash(
            get_markup(
                show_message="Add post error, please try later"
            ), 'danger'
        )

    return redirect(url_for('post.get_post', post_id=post_id))


@post_bp.route('/<int:origin_post>/report/<int:post_id>', methods=['GET'])
def report_post(origin_post: int, post_id: int):
    show_messages = 'Report ok'
    category = 'success'

    user_id = session['user_id']
    post = PostsHandler.get_one_post(post_id)
    if post is not None:
        res = ReportsHandler.add_reports(
            content_id=post_id,
            content=post.content,
            content_type=ReportType.POST,
            accused_id=post.creator.id,
            accuser_id=user_id
        )
        if res is None:
            show_messages = 'Report error'
            category = 'danger'
    else:
        show_messages = 'Empty post'
        category = 'danger'

    flash(
        get_markup(
            show_message=show_messages
        ), category
    )

    return redirect(url_for('post.get_post', post_id=origin_post))
