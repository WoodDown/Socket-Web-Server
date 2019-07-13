from models import Model
from models.base_model import SQLModel
from models.comment import Comment
from utils import log


class Weibo(SQLModel):
    sql_create = '''
        CREATE TABLE `weibo` (
            `id`        INT NOT NULL AUTO_INCREMENT,
            `user_id`   INT NOT NULL,
            `content`   VARCHAR(255) NOT NULL,
            PRIMARY KEY (`id`)
        );
    '''

    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', None)

    @classmethod
    def add(cls, form, user_id):
        form.update(user_id=user_id)
        log('update f', form)
        cls.insert(form)

    def comments(self):
        cs = Comment.all(weibo_id=self.id)
        return cs
