from orm.postgres.model.meta.meta_model import PsqlModelMeta

class BasePsqlModel(metaclass=PsqlModelMeta):
    
    def __init__(self, **kwargs):
        for key in self._meta['fields']:
            print(key)
            setattr(self, key, kwargs.get(key))
    
    def get():
        pass
    
    def create():
        pass
    
    def update():
        pass
    
    def delete():
        pass