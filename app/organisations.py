from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.organisation import Organisation
from models.user import User
import models

org_blueprint = Blueprint('organisation', __name__)

# Get database session
db = models.Storage()
session = db.get_session()

@org_blueprint.route('/organisations', methods=['GET'])
@jwt_required()
def get_organisations():
    user = session.query(User).filter_by(userId=user_id).first()

    if user:
        organisations = [{"orgId": org.orgId, "name": org.name, "description": org.description} for org in user.organisations]
        return jsonify({
            "status": "success",
            "message": "Organisations retrieved successfully",
            "data": {
                "organisations": organisations
            }
        }), 200

    return jsonify({"status": "error", "message": "User not found"}), 404

@org_blueprint.route('/organisations/<org_id>', methods=['GET'])
@jwt_required()
def get_organisation(org_id):
    organisation = session.query(Organisation).filter_by(orgId=org_id).first()

    if organisation:
        return jsonify({
            "status": "success",
            "message": "Organisation retrieved successfully",
            "data": {
                "orgId": organisation.orgId,
                "name": organisation.name,
                "description": organisation.description
            }
        }), 200

    return jsonify({"status": "error", "message": "Organisation not found"}), 404

@org_blueprint.route('/organisations', methods=['POST'])
@jwt_required()
def create_organisation():
    data = request.get_json()
    user_id = get_jwt_identity()

    # Validate required fields
    if not data.get('name'):
        return jsonify({"status": "error", "message": "Name is required"}), 400

    user = session.query(User).filter_by(userId=user_id).first()
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    organisation = Organisation(
        name=data['name'],
        description=data.get('description', '')
    )
    organisation.users.append(user)
    session.add(organisation)
    session.commit()

    return jsonify({
        "status": "success",
        "message": "Organisation created successfully",
        "data": {
            "orgId": organisation.orgId,
            "name": organisation.name,
            "description": organisation.description
        }
    }), 201

@org_blueprint.route('/organisations/<org_id>/users', methods=['POST'])
@jwt_required()
def add_user_to_organisation(org_id):
    data = request.get_json()
    organisation = session.query(Organisation).filter_by(orgId=org_id).first()
    user = session.query(User).filter_by(userId=data['userId']).first()

    if organisation and user:
        organisation.users.append(user)
        session.commit()
        return jsonify({
            "status": "success",
            "message": "User added to organisation successfully"
        }), 200

    return jsonify({"status": "error", "message": "User or Organisation not found"}), 404
