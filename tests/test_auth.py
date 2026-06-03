import pytest
from src.auth import(
    User,
    UserRepository,
    InvalidEmailException,
    InvalidPasswordException,
    UnauthorizedException    
)
class TestUserCreation:
    def test_user_creation_with_all_fields(self)->None:
        user =User(1,'mishree@shopinsight.com','secure_hash_8char','Mishree','Raval','admin')
        assert user.user_id == 1
        assert user.email == 'mishree@shopinsight.com'
        assert user.first_name == "Mishree"
        assert user.last_name == "Raval"
        assert user.role == "admin" 
        
    def test_user_creation_with_defaults(self)->None:
        user= User(2,'minimal@test.com','password_123','john','doe')
        assert user.role == "viewer"
        
    def test_invalid_password_at_construction(self)->None:
        with pytest.raises(InvalidPasswordException):
            User(3,'test@test.com','short','alex','jones')
            
#magic method test
class TesstMagicMehod:
    @pytest.fixture
    def sample_user(self)->User:
        """Provides a pristine, reusable User instance for isolated testing."""
        return User(10,"fixture@test.com",'secure_hash','test','User','shopper')
    
    def test_str_magic_methos(self,sample_user:User)->None:
        assert str(sample_user)=="test User (fixture@test.com)"
      
    def test_repr_magic_method(self,sample_user:User)->None:
        expected_repr = "User(user_id =10,email='fixture@test.com',role='shopper',first_nsme='test',last_name='User')"
        assert repr(sample_user)== expected_repr
        
    def test_qiality_same_id(self,sample_user:User)->None:
        identical_user= User(10,'fixture@test.com','different_hash_same_id','changedname','surname','shopper')
        assert sample_user == identical_user
        
    def test_quality_different_id(self,sample_user:User)->None:
        different_user =User(11,'fixture@test.com','secure_hash_10','test','user','shopper')
        assert sample_user!= different_user
    
    def test_equality_with_non_user(self,sample_user:User)->None:
        assert sample_user != 'not a user object'
    
    def test_less_then_nothing(self,sample_user:User)->None:
        higher_user=User(20,'higher@test.com','secure_hash_20','A','B')
        assert sample_user < higher_user
        
    def test_hash_allows_set_usagw(self,smample_user:User)->None:
        user_set = {sample_user,sample_user} 
        assert len(user_set)==1
#properties,validatio & repository Tests
class TestProperties:
    def test_full_name_property(self)->None:
        user=User(1,"a@b.com","hash_pass","Mishree","Raval")
        assert user.full_name== "Mishree Raval"
    def test_role_property_flags(self) -> None:
        admin = User(1, "a@b.com", "hash_pass", "A", "B", "admin")
        analyst = User(2, "a@b.com", "hash_pass", "A", "B", "analyst")
        viewer = User(3, "a@b.com", "hash_pass", "A", "B", "viewer")
        
        assert admin.is_admin is True
        assert viewer.is_admin is False
        assert analyst.is_analyst is True
        assert admin.is_premium is True
        assert viewer.is_premium is False
    
class TestValidationAndRepository:
    def test_validate_invalid_email_raises_error(self) -> None:
        user = User(1, "bad_email_no_dot@com", "hash_pass_valid", "A", "B")
        with pytest.raises(InvalidEmailException):
            user.validate()
            
    def test_has_permission_hierarchy(self) -> None:
        shopper = User(1, "a@b.com", "hash_pass", "A", "B", "shopper")
        assert shopper.has_permission("viewer") is True
        assert shopper.has_permission("admin") is False
        
    def test_repository_crud_lifecycle(self) -> None:
        repo = UserRepository()
        user = User(1, "test@test.com", "hash_pass_valid", "A", "B", "viewer")
        
        # Test Create
        assert repo.add_user(user) is True
        assert repo.count() == 1
        
        # Test Duplicate Guard
        with pytest.raises(Exception):
            repo.add_user(user)
            
        # Test Read
        assert repo.get_user(1) == user
        assert repo.get_user(99) is None
        
        # Test Delete
        assert repo.delete_user(1) is True
        assert repo.count() == 0          
         