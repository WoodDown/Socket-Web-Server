from models.todo import Todo
from routes import (
    redirect,
    current_user,
    html_response,
    login_required,
)
from utils import log


def index(request):
    log('routes todo index')
    u = current_user(request)
    todos = Todo.find_all(user_id=u.id)
    return html_response('todo_index.html', todos=todos)


def add(request):
    log('routes todo add')
    u = current_user(request)
    form = request.form()
    Todo.add(form, u.id)
    return redirect('/todo/index')


def delete(request):
    log('routes todo delete')
    todo_id = int(request.query['id'])
    Todo.delete(todo_id)
    return redirect('/todo/index')


def edit(request):
    log('routes todo edit')
    todo_id = int(request.query['id'])
    t = Todo.find_by(id=todo_id)
    return html_response('todo_edit.html', todo=t)


def update(request):
    log('routes todo update')
    form = request.form()
    Todo.update(form)
    return redirect('/todo/index')


def same_user_required(route_function):
    def f(request):
        log('required same_user')
        u = current_user(request)
        if 'id' in request.query:
            todo_id = request.query['id']
        else:
            todo_id = request.form()['id']
        t = Todo.find_by(id=int(todo_id))

        if t.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/todo/index')

    return f


def route_dict():
    d = {
        '/todo/add': login_required(add),
        '/todo/delete': login_required(same_user_required(delete)),
        '/todo/edit': login_required(same_user_required(edit)),
        '/todo/update': login_required(same_user_required(update)),
        '/todo/index': login_required(index),
    }
    return d
