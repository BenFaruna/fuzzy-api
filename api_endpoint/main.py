import os

from dotenv import load_dotenv

from flask import jsonify, request

from api_endpoint.utils import (
    create_app, create_database_session, validate_url_parameter
    )
from api_endpoint.models.person import Person

load_dotenv()


app = create_app()
engine, session = create_database_session()


@app.route("/api/<string:name>", methods=["GET"], strict_slashes=False)
def get_user(name):
    # Todo: validation of parameter data type
    try:
        if not validate_url_parameter(name):
            raise ValueError(
                "/api/<name> - all characters in <name> should be alphabets"
                )
    except ValueError as e:
        session.rollback()
        return jsonify({"Error": str(e)}), 400


    try:
        person = session.query(Person).filter(Person.name == name).first()

        if person:
            return jsonify(person.to_dict())
        else:
            return jsonify({"Error": f"{name} not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"Error": str(e)})


@app.route("/api", methods=["POST"], strict_slashes=False)
def create_user():
    body = request.get_json(force=True, silent=True)

    if not body or "name" not in body:
        return jsonify({"Error": "body data not supplied or name key not found"}), 400

    try:
        new_person = Person(**body)
        session.add(new_person)
        session.commit()
        user = session.query(Person).filter(Person.name == body.get("name")).first()
        return jsonify({"Success": "New user added", "user": user.to_dict()}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"Error": "Name already exists"}), 403


@app.route("/api/<string:name>", methods=["PUT"], strict_slashes=False)
def update_name(name):
    try:
        if not validate_url_parameter(name):
            raise ValueError(
                "/api/<name> - all characters in <name> should be alphabets"
                )
    except ValueError as e:
        return jsonify({"Error": str(e)}), 400

    body = request.get_json()

    user = session.query(Person).filter(Person.name == name).first()

    if not user:
        return jsonify({"Error": f"{name} not found"}), 404

    try:
        if user and body.get("new_name"):
            user.name = body.get("new_name")
            session.commit()
            user = session.query(Person).filter(Person.name == body.get("new_name")).first()
            return jsonify({"Success": "Name updated", "user": user.to_dict()})
        else:
            return jsonify({"Error": "new_name data not supplied"}), 400
    except Exception as e:
        print(str(e))
        session.rollback()
        return jsonify({"Error": "Name already exists"}), 403


@app.route("/api/<string:name>", methods=["DELETE"], strict_slashes=False)
def delete_user(name):
    try:
        if not validate_url_parameter(name):
            raise ValueError(
                "/api/<name> - all characters in <name> should be alphabets"
                )
    except ValueError as e:
        return jsonify({"Error": str(e)}), 400

    user = session.query(Person).filter(Person.name == name).first()

    if not user:
        return jsonify({"Error": f"{name} not found"}), 404

    try:
        session.delete(user)
        session.commit()
    except Exception as e:
        session.rollback()
        return jsonify({"Error": str(e)}), 500

    return jsonify({"Success": f"{name} deleted"})


if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG"))
