"""
Authentication and Authorization Module for the ShopInsight Platform.
Provides advanced object-oriented user modeling, secure state encapsulation,
and a distinct custom application exception hierarchy.
"""
class ShopInsightError(Exception):
    "base exception class for all custom operations in the hshopinsight plateform"
    def __init__(self,message:str,code:int = 400):
        super().__init__(message)
        self.message = message
        self.code = code
    
    def __str__(self) -> str:
        #return a clean,readable presentation layout  for logging and end users
        return f"[{self.code}] {self.message}"
    
class UnauthorizedException(ShopInsightError):
    """raised when authentication credentials fail or user lacks access permision"""
    def __init__(self,message:str = "unauthorized access attempt"):
        super().__init__(message,code=401)
        
class InvalidEmailException(ShopInsightError):
    """raised when an email address formate validation check fails."""
    def __init__(self,message: str = "provided email formate is invalid."):
        super().__init__(message,code=422)
        
class UserAlreadyExistsException(ShopInsightError):
    """raised during registraiton if an identity collision occurs in memory storage."""
    def __init__(slef,message : str = "a user account with detial alreay exosts"):
        super().__init__(message,code=409)
        
class InvalidPasswordException(ShopInsightError):
    """raised when a password fails minimum strctural strength requirements."""
    def __init__(self,message: str = "password does not satisfy minimum length rule"):
        super().__init__(message,code=400)
         
class User:
    #class level immutable configuration constants
    MIN_PASSWORD_LOGIN_LENGTH:int = 8
    VALID_ROLES:list[str]=["shopper","admin","viewer","analyst"]
    
    def __init__(self,user_id:int,email:str,password_hash:str,first_name: str,last_name:str,role:str="viewer"):
        if len(password_hash)< self.MIN_PASSWORD_LOGIN_LENGTH:
            raise InvalidPasswordException(f"password must be at least {self.MIN_PASSWORD_LOGIN_LENGTH} characters.")
        if role not in self.VALID_ROLES:
            raise UnauthorizedException(f"invalid system role provided:{role}")
        #state binding using explicit type annotations
        
        self.user_id: int = user_id
        self.email:str =email
        self.password_hash:str= password_hash
        self.first_name : str=first_name
        self.last_name: str = last_name
        self.role:str = role
        
    def __str__(self)->str:
        return f"{self.first_name} {self.last_name} ({self.email})"
        
    def __repr__(self)->str:

        return f"User(user_id={self.user_id},email='{self.email}',role='{self.role}',first_name='{self.first_name}',last_name='{self.last_name}')"

    def __eq__(self,other)-> bool:
        if not isinstance(other,User):
            return NotImplemented
        return self.user_id == other.user_id and self.email == other.email
    
    def __lt__(self,other)->bool:
        if not isinstance(other,User):
            return NotImplemented
        return self.user_id<other.user_id
    
    def __hash__(self)-> int:
        return hash((self.user_id,self.email))
    
    def __le__(self,other)->bool:
        return self.user_id <= other.user_id
#ENCAPSULATED COMPUTED PROPERTIES

    @property
    def full_name(self)-> str:
        """dynamically computes the user's full name from strcural parts"""
        return f"{self.first_name}{self.last_name}"

    @property
    def is_admin(self)-> bool:
        """read only flag derived immediately from the string state of the account role"""
        return self.role == "admin"

    @property
    def is_analyst(self)-> bool:
        """determines if the accounts belongs to the analyst security domain group"""
        return self.role == "analyst"

    @ property
    def is_premium(self)-> bool:
        """checks if the account role holds advanced premium access permission"""
        return self.role in ["admin","analyst"]

    #validation & security utilities

    @staticmethod
    def _is_valid_email(email:str)->bool:
        """Decoupled string validation utility function checking structural email format."""
        return "@" in email and "." in email.split("@")[-1]

    def validate(self)->bool:
        """Runs validation checks across instance attributes and flags irregularities."""
        if not self._is_valid_email(self.email):
            raise InvalidEmailException(f"format verifiaction failed for : {self.email}")
        return True

    def has_permission(self,required_role:str)->bool:
        """Evaluates whether the user's role meets or exceeds structural access requirements."""
            # Simple tier-matching hierarchy logic rule
        role_hierarchy = {"viewer":1,"shopper":2,"analyst":3,"admin":4}
        user_rank = role_hierarchy.get(self.role,0)
        required_rank = role_hierarchy.get(required_role,5)
        
        return user_rank >= required_rank

    #SERIALIZATION

    def to_dict(self)-> dict:
        """Serializes internal instance states into a standard Python dictionary format.""" 
        return{
            "user_id":self.user_id,
            "email":self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role,
            "full_name": self.full_name
        }
        