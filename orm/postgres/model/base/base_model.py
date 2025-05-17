from orm.postgres.model.meta.meta_model import PsqlModelMeta

from orm.postgres.driver.driver import PostgresDriver
from utils.static.privacy.privacy import privatemethod

class BasePsqlModel(metaclass=PsqlModelMeta):
    
    def __init__ (
        self, 
        **kwargs,
    ) -> None:
        
        for key in self._meta['fields']:
            setattr(self, key, kwargs.get(key)) 
    
    async def select (
        self, 
        **filters,
    ) -> None:
        
        self._verify_filters(filters, 'SELECT')
        
        with PostgresDriver() as cursor:
            where_clause = " AND ".join(f"{k} = %s" for k in filters)
            query = f"""
            SELECT * 
            FROM {self._meta['table_name']} 
            WHERE {where_clause} LIMIT 1;
            """
            values = tuple(filters.values())
            
            await cursor.execute(query, values)
        
    def selectOne (
        self, 
        **filters,
    ) -> None:
        
        self._verify_filters(filters, 'SELECT')
        
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
        
        self._verify_filters(filters, 'SELECT')
        
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
    
    def delete (
        self,
        **filters,
    ) -> None:
        
        self._verify_filters(filters, 'DELETE')
        
        where_clause = " AND ".join(f"{k} = %s" for k in filters)
        query = f"""
        DELETE  
        FROM {self._meta['table_name']} 
        WHERE {where_clause};
        """
    
    @privatemethod
    def _verify_filters (
        self, 
        filters, 
        operation_name,
    ) -> None:
        
        if not filters:
            raise ValueError(f"{operation_name} with no filters is unsafe")