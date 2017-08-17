class MySqlRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "mysql":
            return "mysql"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "mysql":
            return "mysql"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'mysql' or \
           obj2._meta.app_label == 'mysql':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'mysql':
            return db == 'mysql'
        return None


class FioRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "fiotest":
            return "default"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "fiotest":
            return "default"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'fiotest' or \
           obj2._meta.app_label == 'fiotest':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'fiotest':
            return db == 'default'
        return None

