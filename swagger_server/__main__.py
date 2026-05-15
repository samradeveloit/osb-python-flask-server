#!/usr/bin/env python3

import connexion
from flask import jsonify, make_response, request

from swagger_server.controllers import authorization_controller
from swagger_server.controllers import service_instances_controller
from swagger_server import encoder


def _unauthorized_response():
    return make_response(jsonify({
        "detail": "No valid authorization token provided",
        "status": 401,
        "title": "Unauthorized",
        "type": "about:blank",
    }), 401)


def _serialize_controller_result(result):
    status_code = 200
    payload = result

    if isinstance(result, tuple):
        payload = result[0]
        status_code = result[1]

    response = make_response(jsonify(payload), status_code)
    return response


def _authorized():
    auth_header = request.headers.get("Authorization")
    return authorization_controller.check_bearer_crn(auth_header, [])


def _register_encoded_instance_routes(flask_app):
    def provision_encoded_instance(instance_id):
        if not _authorized():
            return _unauthorized_response()
        return _serialize_controller_result(
            service_instances_controller.service_instance_provision(
                instance_id=instance_id,
                X_Broker_API_Version=request.headers.get("X-Broker-API-Version"),
                X_Broker_API_Originating_Identity=request.headers.get("X-Broker-API-Originating-Identity"),
                X_Broker_API_Request_Identity=request.headers.get("X-Broker-API-Request-Identity"),
                accepts_incomplete=request.args.get("accepts_incomplete"),
            )
        )

    def get_encoded_instance(instance_id):
        if not _authorized():
            return _unauthorized_response()
        return _serialize_controller_result(
            service_instances_controller.service_instance_get(
                instance_id=instance_id,
                X_Broker_API_Version=request.headers.get("X-Broker-API-Version"),
                X_Broker_API_Originating_Identity=request.headers.get("X-Broker-API-Originating-Identity"),
                X_Broker_API_Request_Identity=request.headers.get("X-Broker-API-Request-Identity"),
                service_id=request.args.get("service_id"),
                plan_id=request.args.get("plan_id"),
            )
        )

    def update_encoded_instance(instance_id):
        if not _authorized():
            return _unauthorized_response()
        return _serialize_controller_result(
            service_instances_controller.service_instance_update(
                instance_id=instance_id,
                X_Broker_API_Version=request.headers.get("X-Broker-API-Version"),
                X_Broker_API_Originating_Identity=request.headers.get("X-Broker-API-Originating-Identity"),
                X_Broker_API_Request_Identity=request.headers.get("X-Broker-API-Request-Identity"),
                accepts_incomplete=request.args.get("accepts_incomplete"),
            )
        )

    def delete_encoded_instance(instance_id):
        if not _authorized():
            return _unauthorized_response()
        return _serialize_controller_result(
            service_instances_controller.service_instance_deprovision(
                instance_id=instance_id,
                X_Broker_API_Version=request.headers.get("X-Broker-API-Version"),
                X_Broker_API_Originating_Identity=request.headers.get("X-Broker-API-Originating-Identity"),
                X_Broker_API_Request_Identity=request.headers.get("X-Broker-API-Request-Identity"),
                service_id=request.args.get("service_id"),
                plan_id=request.args.get("plan_id"),
                accepts_incomplete=request.args.get("accepts_incomplete"),
            )
        )

    def last_operation_encoded_instance(instance_id):
        if not _authorized():
            return _unauthorized_response()
        return _serialize_controller_result(
            service_instances_controller.service_instance_last_operation_get(
                instance_id=instance_id,
                X_Broker_API_Version=request.headers.get("X-Broker-API-Version"),
                X_Broker_API_Originating_Identity=request.headers.get("X-Broker-API-Originating-Identity"),
                X_Broker_API_Request_Identity=request.headers.get("X-Broker-API-Request-Identity"),
                service_id=request.args.get("service_id"),
                plan_id=request.args.get("plan_id"),
                operation=request.args.get("operation"),
            )
        )

    flask_app.add_url_rule(
        "/v2/service_instances/<path:instance_id>/last_operation",
        "last_operation_encoded_instance",
        last_operation_encoded_instance,
        methods=["GET"],
    )
    flask_app.add_url_rule(
        "/v2/service_instances/<path:instance_id>",
        "provision_encoded_instance",
        provision_encoded_instance,
        methods=["PUT"],
    )
    flask_app.add_url_rule(
        "/v2/service_instances/<path:instance_id>",
        "get_encoded_instance",
        get_encoded_instance,
        methods=["GET"],
    )
    flask_app.add_url_rule(
        "/v2/service_instances/<path:instance_id>",
        "update_encoded_instance",
        update_encoded_instance,
        methods=["PATCH"],
    )
    flask_app.add_url_rule(
        "/v2/service_instances/<path:instance_id>",
        "delete_encoded_instance",
        delete_encoded_instance,
        methods=["DELETE"],
    )


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Open Service Broker API'}, pythonic_params=True)
    _register_encoded_instance_routes(app.app)
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
