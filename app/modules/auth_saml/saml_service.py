# app/modules/auth_saml/saml_service.py
# Este módulo implementa la lógica de autenticación SAML utilizando
# la biblioteca OneLogin.

from fastapi import Request
from onelogin.saml2.auth import OneLogin_Saml2_Auth


def prepare_request(request: Request):
    form_data = {}
    return {
        "https": "on" if request.url.scheme == "https" else "off",
        "http_host": request.url.hostname,
        "server_port": request.url.port,
        "script_name": request.url.path,
        "get_data": dict(request.query_params),
        "post_data": form_data,
    }


def get_saml_auth(request: Request, settings):
    req = prepare_request(request)
    return OneLogin_Saml2_Auth(req, settings)
