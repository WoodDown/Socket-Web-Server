import pymysql

import config
import secret
from utils import log


class SQLModel(object):
    connection = None

    @classmethod
    def init_db(cls):
        cls.connection = pymysql.connect(
            host='localhost',
            user='root',
            password=secret.mysql_password,
            db=config.db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def __init__(self, form):
        self.id = form.get('id', None)

    @classmethod
    def table_name(cls):
        return '`{}`'.format(cls.__name__)

    @classmethod
    def new(cls, form):
        m = cls(form)
        id = cls.insert(m.__dict__)
        m.id = id
        return m

    @classmethod
    def insert(cls, form):
        if 'id' in form:
            form.pop('id')

        sql_keys = ', '.join(['`{}`'.format(k) for k in form.keys()])
        sql_values = ', '.join(['%s'] * len(form))
        sql_insert = 'INSERT INTO {} ({}) VALUES ({})'.format(
            cls.table_name(),
            sql_keys,
            sql_values,
        )

        log('ORM insert <{}>'.format(sql_insert))

        values = tuple(form.values())

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_insert, values)
            _id = cursor.lastrowid
        cls.connection.commit()

        return _id

    @classmethod
    def delete(cls, id):
        sql_delete = 'DELETE FROM {} WHERE `id`=%s'.format(cls.table_name())
        log('ORM delete <{}>'.format(sql_delete.replace('\n', ' ')))

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_delete, (id,))
        cls.connection.commit()

    @classmethod
    def update(cls, id, **kwargs):
        sql_set = ', '.join(
            ['`{}`=%s'.format(k) for k in kwargs.keys()]
        )
        sql_update = 'UPDATE {} SET {} WHERE `id`=%s'.format(
            cls.table_name(),
            sql_set,
        )
        log('ORM update <{}>'.format(sql_update.replace('\n', ' ')))

        values = list(kwargs.values())
        values.append(id)
        values = tuple(values)

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_update, values)
        cls.connection.commit()

    @classmethod
    def one(cls, **kwargs):
        search = ' AND '.join(
            ['`{}`=%s'.format(k) for k in kwargs.keys()]
        )

        values = tuple(kwargs.values())

        sql_search = 'SELECT * FROM {} WHERE {}'.format(
            cls.table_name(),
            search,
        )

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_search, values)
            result = cursor.fetchone()
            log('sql search result', result, type(result))
            if result is None:
                return None
            else:
                return cls(result)

    @classmethod
    def all(cls, **kwargs):
        # 查询的字段
        search = ' AND '.join(
            ['`{}`=%s'.format(k) for k in kwargs.keys()]
        )

        # 查询的字段的值
        values = tuple(kwargs.values())

        # 查询条件判断
        if len(kwargs) > 0:
            sql_search = 'SELECT * FROM {} WHERE {}'.format(
                cls.table_name(),
                search,
            )
        else:
            sql_search = 'SELECT * FROM {}'.format(
                cls.table_name(),
            )

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_search, values)
            # 查询返回所有结果
            result = cursor.fetchall()
            log('sql search result', result, type(result))
            if result is None:
                return None
            else:
                # 实例化所有对象
                models = []
                for form in result:
                    models.append(cls(form))
                return models

    def __repr__(self):
        name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(name, s)

    def json(self):
        return self.__dict__
