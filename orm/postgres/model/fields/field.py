class Field:
    
    def __init__ (
        self,
        column_type,
        primary_key=False,
    ) -> None:
        
        self.column_type = column_type
        self.primary_key = primary_key