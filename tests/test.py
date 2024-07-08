import unittest
import json
from app import create_app
from models.user import User
from models.organisation import Organisation
#from models.token import Token
from datetime import datetime, timedelta
from passlib.hash import bcrypt
from models.storage import Storage

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test case."""
        self.app = create_app()
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Initialize database by creating mapped tables
        self.db = Storage()
        self.session = self.db.get_session()

    def tearDown(self):
        """Tear down the test case."""
        self.session.remove()
        self.db.drop_all()
        self.app_context.pop()

    def test_register_user_successfully(self):
        """It Should Register User Successfully with Default Organisation"""
        user_data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "securepassword",
            "phone": "123456789"
        }
        response = self.client().post('/auth/register', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        #self.assertIn('access_token', response_data)
        self.assertIsNotNone(response_data['data']['accessToken'])
        self.assertEqual(response_data['data']['user']['firstName'], "John")
        self.assertEqual(response_data['data']['user']['lastName'], "Doe")
        self.assertEqual(response_data['data']['user']['email'], "john.doe@example.com")
        self.assertEqual(response_data['data']['organisation']['name'], "John's Organisation")
"""
    def test_login_user_successfully(self):
        It Should Log the user in successfully
        user = User(firstName="John", lastName="Doe", email="john.doe@example.com")
        user.hash_password("securepassword")
        db.session.add(user)
        db.session.commit()

        login_data = {
            "email": "john.doe@example.com",
            "password": "securepassword"
        }
        response = self.client().post('/auth/login', data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('access_token', response_data)
        self.assertEqual(response_data['user']['email'], "john.doe@example.com")

    def test_register_user_missing_fields(self):
        It Should Fail If Required Fields Are Missing
        incomplete_user_data = {
            "firstName": "John",
            "email": "john.doe@example.com",
            "password": "securepassword"
        }
        response = self.client().post('/auth/register', data=json.dumps(incomplete_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 422)
        response_data = json.loads(response.data)
        self.assertIn('lastName', response_data['errors'])

    def test_register_user_duplicate_email(self):
        It Should Fail if there’s Duplicate Email
        user = User(firstName="John", lastName="Doe", email="john.doe@example.com")
        user.hash_password("securepassword")
        db.session.add(user)
        db.session.commit()

        duplicate_user_data = {
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "securepassword"
        }
        response = self.client().post('/auth/register', data=json.dumps(duplicate_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 422)
        response_data = json.loads(response.data)
        self.assertIn('email', response_data['errors'])

    def test_token_generation(self):
        Token generation - Ensure token expires at the correct time and correct user details are found in the token.
        user = User(firstName="John", lastName="Doe", email="john.doe@example.com")
        user.hash_password("securepassword")
        db.session.add(user)
        db.session.commit()

        token = Token.generate_auth_token(user.id)
        self.assertIsNotNone(token)

        user_id = Token.verify_auth_token(token)
        self.assertEqual(user_id, user.id)

        token_data = Token.decode_auth_token(token)
        expiration = token_data['exp']
        expected_expiration = datetime.utcnow() + timedelta(hours=1)
        self.assertAlmostEqual(expiration, expected_expiration, delta=timedelta(minutes=1))

    def test_organisation_data_access(self):
        Organisation - Ensure users can’t see data from organisations they don’t have access to.
        user1 = User(firstName="John", lastName="Doe", email="john.doe@example.com")
        user1.hash_password("securepassword")
        user2 = User(firstName="Jane", lastName="Doe", email="jane.doe@example.com")
        user2.hash_password("securepassword")
        organisation1 = Organisation(name="Org1")
        organisation2 = Organisation(name="Org2")
        organisation1.users.append(user1)
        organisation2.users.append(user2)
        db.session.add_all([user1, user2, organisation1, organisation2])
        db.session.commit()

        login_data = {
            "email": "john.doe@example.com",
            "password": "securepassword"
        }
        response = self.client().post('/auth/login', data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        token = response_data['access_token']

        headers = {'Authorization': f'Bearer {token}'}
        response = self.client().get(f'/api/organisations/{organisation2.id}', headers=headers)
        self.assertEqual(response.status_code, 403)
"""

if __name__ == "__main__":
    unittest.main()
