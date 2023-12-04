from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app

from app.hyldb.handler.channels import ChannelsHandler
from app.hyldb.handler.posts import PostsHandler
from app.hyldb.handler.users import UserHandler
from app.utils.generate_template import get_markup

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index(active_label=1):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    username = session.get('username')
    if username is None:
        return redirect(url_for('auth.login'))

    user, ok = UserHandler.get_user_by_id(user_id=user_id)
    if not ok:
        flash(
            get_markup(
                show_message="Internal error"
            ),
            'warning'
        )
        current_app.logger.error("User find error")
        return redirect(url_for('main.index'))
    else:
        if user is None:
            session.clear()
            return redirect(url_for("main.index"))
        else:
            # channels = UserHandler.get_channels_info(username)
            channels, ok = ChannelsHandler.get_all_channels()

            if not ok:
                return "Internal Error", 500

            posts = PostsHandler.get_all_posts(filter_normal=True)

            if posts is None:
                return render_template(
                    'error.html'
                )

            # current_app.logger.info(f"Get channels: {channels}")
            last_visit = session.get('last_visit')

            label = request.args.get('active_label')
            if label is not None:
                active_label = int(label)
            return render_template(
                "channels.html",
                user_id=user_id,
                username=username,
                channels=channels,
                last_visit=last_visit,
                posts=posts,
                active_label=active_label
            )
