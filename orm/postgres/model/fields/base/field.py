class Field:
    
    def __init__ (
        self,
        column_type,
        primary_key=False,
    ) -> None:
        
        self.column_type = column_type
        self.primary_key = primary_key
        
        self.name = None
        self.owner = None
        
    def __set_name__ (
        self,
        owner,
        name,
    ) -> None:
        
        self.name = name
        self.owner = owner
        
    def __get__ (
        self,
        instance,
        owner,
    ) -> None:
        
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__ (
        self, 
        instance, 
        value,
    ) -> None:
        
        instance.__dict__[self.name] = value