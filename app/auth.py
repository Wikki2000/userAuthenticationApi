from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models.user import User
from models.organisation import Organisation
from flask_jwt_extended import create_access_token
import models


# Initialized database by creating tables
storage = models.Storage()
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ["firstName", "lastName", "email", "password"]

    # Validate required fields
    errors = []
    for field in required_fields:
        if not data.get(field):
            errors.append({"field": field, "message": f"{field} is required"})

    if errors:
        return jsonify({"errors": errors}), 422


    # Create User
    try:
        user = User(
            firstName=data['firstName'],
            lastName=data['lastName'],
            email=data['email'],
            password=data['password'],
            phone=data.get('phone')
        )
        user.hash_password(data['password'])
        user.save()

        # Create Default Organisation
        org_name = f"{user.firstName}'s Organisation"
        organisation = Organisation(name=org_name)
        organisation.users.append(user)
        organisation.save()

        access_token = create_access_token(identity=user.userId)
        return jsonify({
            "status": "success",
            "message": "Registration successful",
            "data": {
                "accessToken": access_token,
                "user": {
                    "userId": user.userId,
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "phone": user.phone,
                }
            }
        }), 201

    except IntegrityError:
        session = user.get_session()
        session.rollback()

        return jsonify({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 400
        }), 400

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.get_user_email(email).one()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.userId)
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "data": {
                "accessToken": access_token,
                "user": {
                    "userId": user.userId,
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "phone": user.phone,
                }
            }
        }), 200

    return jsonify({
        "status": "Bad request",
        "message": "Authentication failed",
        "statusCode": 401
    }), 401
