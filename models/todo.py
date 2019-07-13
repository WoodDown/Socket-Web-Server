from models import Model


class Todo(Model):
    def __init__(self, form):
        super().__init__(form)
        self.title = form.get('title', '')
        self.user_id = form.get('user_id', None)

    @classmethod
    def add(cls, form, user_id):
        t = Todo(form)
        t.user_id = user_id
        t.save()

    @classmethod
    def update(cls, form):
        todo_id = int(form['id'])
        t = Todo.find_by(id=todo_id)
        t.title = form['title']
        t.save()
