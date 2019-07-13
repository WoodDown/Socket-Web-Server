from utils import log
from routes import current_user, redirect, html_response, login_required
from models.comment import Comment


def add(request):
    log('routes comment add')
    u = current_user(request)

    form = request.form()
    weibo_id = int(form['weibo_id'])
    content = form['content']

    form = dict(
        id=None,
        user_id=u.id,
        weibo_id=weibo_id,
        content=content,
    )
    Comment.insert(form)

    return redirect('/weibo/index')


def delete(request):
    log('routes comment delete')
    comment_id = int(request.query['id'])
    Comment.delete(comment_id)

    return redirect('/weibo/index')


def edit(request):
    log('routes comment edit')
    comment_id = int(request.query['id'])
    c = Comment.one(id=comment_id)

    return html_response('comment_edit.html', comment=c)


def update(request):
    log('routes comment update')
    form = request.form()

    id = int(form['id'])
    content = form['content']
    Comment.update(id, content=content)

    return redirect('/weibo/index')


def comment_owner_required(route_function):
    def f(request):
        log('required comment owner')
        u = current_user(request)
        if 'id' in request.query:
            comment_id = request.query['id']
        else:
            comment_id = request.form()['id']
        c = Comment.one(id=int(comment_id))
        log('user comment_id comment', u, comment_id, c)

        if c.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/weibo/index')

    return f


def route_dict():
    d = {
        '/comment/add': login_required(add),
        '/comment/delete': login_required(comment_owner_required(delete)),
        '/comment/edit': login_required(comment_owner_required(edit)),
        '/comment/update': login_required(update),
    }
    return d
