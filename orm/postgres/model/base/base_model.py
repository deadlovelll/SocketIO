from orm.postgres.model.meta.meta_model import PsqlModelMeta

class BasePsqlModel(metaclass=PsqlModelMeta):
    
    def __init__ (
        self, 
        **kwargs,
    ) -> None:
        
        for key in self._meta['fields']:
            setattr(self, key, kwargs.get(key))
    
    def get():
        pass
    
    def create (
        self,
    ) -> None:
        
        fields = self._meta['fields']
        values = [getattr(self, f) for f in fields]
        placeholders = ','.join(['%s'] * len(fields)) 
        query = f"""
        INSERT INTO {self._meta['table_name']}
        ({', '.join(fields)})
        VALUES ({placeholders})
        """
    
    def update():
        pass
    
    def delete():
        pass