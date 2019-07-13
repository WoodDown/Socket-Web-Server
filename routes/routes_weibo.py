from models.comment import Comment
from models.weibo import Weibo
from routes import (
    redirect,
    current_user,
    html_response,
    login_required,
)
from utils import log


def index(request):
    log('routes weibo index')
    u = current_user(request)

    weibos = Weibo.all(user_id=u.id)

    return html_response('weibo_index.html', weibos=weibos, user=u)


def add(request):
    log('routes weibo add')
    u = current_user(request)

    form = request.form()
    Weibo.add(form, u.id)

    return redirect('/weibo/index')


def delete(request):
    log('routes weibo delete')
    weibo_id = int(request.query['id'])

    cs = Comment.all(weibo_id=weibo_id)
    for c in cs:
        c.delete(c.id)

    Weibo.delete(weibo_id)

    return redirect('/weibo/index')


def edit(request):
    log('routes weibo edit')
    weibo_id = int(request.query['id'])
    w = Weibo.one(id=weibo_id)

    return html_response('weibo_edit.html', weibo=w)


def update(request):
    log('routes weibo update')
    form = request.form()

    id = form['id']
    content = form['content']
    Weibo.update(id, content=content)

    return redirect('/weibo/index')


def weibo_owner_required(route_function):
    def f(request):
        log('required weibo_owner')
        u = current_user(request)
        if 'id' in request.query:
            weibo_id = request.query['id']
        else:
            weibo_id = request.form()['id']
        w = Weibo.one(id=int(weibo_id))
        # log('<user> <weibo id> <weibo>', u, weibo_id, w)

        if w.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/weibo/index')

    return f


def route_dict():
    d = {
        '/weibo/add': login_required(add),
        '/weibo/delete': login_required(weibo_owner_required(delete)),
        '/weibo/edit': login_required(weibo_owner_required(edit)),
        '/weibo/update': login_required(weibo_owner_required(update)),
        '/weibo/index': login_required(index),
    }
    return d
