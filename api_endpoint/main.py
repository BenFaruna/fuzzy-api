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
        return jsonify({"Error": str(e)}), 400


    person = session.query(Person).filter(Person.name == name).first()

    if person:
        return jsonify(person.to_dict())
    else:
        return jsonify({"Error": f"{name} not found"}), 404

@app.route("/api", methods=["POST"], strict_slashes=False)
def create_user():
    body = request.get_json()

    try:
        new_person = Person(**body)
        session.add(new_person)
        session.commit()
        return jsonify({"Success": "New user added"})
    except Exception as e:
        session.rollback()
        return jsonify({"Error": str(e)}), 500


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
        else:
            return jsonify({"Error": "new name not supplied"}), 400
    except Exception as e:
        session.rollback()
        return jsonify({"Error": str(e)}), 500

    return jsonify({"Success": "Name updated!"})


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
        return jsonify({"Error": f"{name} cannot be found"}), 404

    try:
        session.delete(user)
        session.commit()
    except Exception as e:
        session.rollback()
        return jsonify({"Error": str(e)}), 500

    return jsonify({"Success": f"{name} deleted!"})


if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG"))
