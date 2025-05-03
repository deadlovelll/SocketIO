from SocketIO.orm.postgres.model.fields.base.field import Field

class PsqlModelMeta(type):
    
    def __new__ (
        cls,
        name,
        bases,
        attrs,
    ) -> None:
        
        if name == 'BaseModel':
            return super().__init__ (
                cls,
                name,
                bases,
                attrs,
            )
            
        fields = {}
        for k, v in attrs.items():
            if isinstance(v, Field):
                fields[k] = v
        
        for k in fields:
            attrs.pop(k)
            
        attrs['_meta'] = {
            'table_name': name.lower(),
            'fields': fields,
        }

        return super().__new__(cls, name, bases, attrs)