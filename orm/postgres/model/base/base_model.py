from orm.postgres.model.meta.meta_model import PsqlModelMeta

class BasePsqlModel(metaclass=PsqlModelMeta):
    
    def __init__ (
        self, 
        **kwargs,
    ) -> None:
        
        for key in self._meta['fields']:
            setattr(self, key, kwargs.get(key)) 
    
    def select (
        self, 
        **filters,
    ) -> None:
        
        where_clause = " AND ".join(f"{k} = %s" for k in filters)
        query = f"""
        SELECT * 
        FROM {self._meta['table_name']} 
        WHERE {where_clause} LIMIT 1;
        """
        values = tuple(filters.values())
        
    def selectOne (
        self, 
        **filters,
    ) -> None:
        
        where_clause = " AND ".join(f"{k} = %s" for k in filters)
        query = f"""
        SELECT * 
        FROM {self._meta['table_name']} 
        WHERE {where_clause} LIMIT 1;
        """
        values = tuple(filters.values())
        
    def selectMany (
        self, 
        **filters,
    ) -> None:
        
        where_clause = " AND ".join(f"{k} = %s" for k in filters)
        query = f"""
        SELECT * 
        FROM {self._meta['table_name']} 
        WHERE {where_clause};
        """
        values = tuple(filters.values())

    def insert (
        self,
    ) -> None:
        
        fields = self._meta['fields']
        values = [getattr(self, f) for f in fields]
        placeholders = ','.join(['%s'] * len(fields)) 
        query = f"""
        INSERT INTO {self._meta['table_name']}
        ({', '.join(fields)})
        VALUES ({placeholders});
        """
    
    def update():
        pass
    
    def delete():
        pass