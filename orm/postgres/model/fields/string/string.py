from orm.postgres.model.fields.field import Field

class VarChar(Field):
    
    def __init__ (
        self, 
        length: int = 255, 
        non_null: bool = False, 
        default: bool = False,
    ) -> None:
        
        super().__init__('VARCHAR', False)
        
        self.length = length
        self.non_null = non_null
        self.default = default
     
       
class CharacterVarying(Field):
    
    def __init__ (
        self, 
        length: int = 255, 
        non_null: bool = False, 
        default: bool = False,
    ) -> None:
        
        super().__init__('CHARACTER VARYING', False)
        
        self.length = length
        self.non_null = non_null
        self.default = default