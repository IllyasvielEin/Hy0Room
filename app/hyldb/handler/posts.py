from flask import current_app
from sqlalchemy import and_, not_, null

from app.hyldb.models.posts import Posts, PostState


class PostsHandler:

    @staticmethod
    def get_one_post(post_id: int):
        res = Posts.get_one_by_id(oid=post_id)
        return res

    @staticmethod
    def get_all_posts(filter_normal=False):
        try:
            if filter_normal:
                res = Posts.query.filter(and_(Posts.parent_id == Posts.id, Posts.state == PostState.NORMAL)).all()
            else:
                res = Posts.get()
        except Exception as e:
            current_app.logger.error(f"{e}")
            res = None
        return res

    @staticmethod
    def add_post(user_id: int, content: str, title: None | str = None, parent_id: int | None = None):
        ok = True
        try:
            if parent_id == -1:
                res = Posts.add(user_id=user_id, title=title, content=content)
                Posts.update(oid=res.id, kv={
                    'parent_id': res.id
                })
            else:
                res = Posts.add(user_id=user_id, title=title, content=content, parent_id=parent_id)
        except Exception as e:
            current_app.logger.error(f"{e}")
            res = None
            ok = False
        return res, ok

    @staticmethod
    def set_parent(post_id: int, parent_id: int):
        _, ok = Posts.update(
            oid=post_id,
            kv={
                'parent_id': parent_id
            }
        )
        return ok

    @staticmethod
    def modify_post(post_id: int, new_content: str):

        _, ok = Posts.update(
            oid=post_id, kv={
                'content': new_content
            })

        return ok

    @staticmethod
    def delete_post(post_id: int):

        _, ok = Posts.update(
            oid=post_id, kv={
                'state': PostState.DELETE
            }
        )

        return ok

    @staticmethod
    def judge_post(post_id: int, guilty: bool):

        state = PostState.FORBIDDEN if guilty else PostState.NORMAL
        current_app.logger.info(state.name)
        _, ok = Posts.update(
            oid=post_id,
            kv={
                'state': state
            }
        )

        return ok
