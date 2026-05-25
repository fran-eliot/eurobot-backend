# app/modules/auth_saml/saml_config.py

# Este módulo define la configuración SAML para el proveedor de identidad (IdP) y/o
# proveedor de servicio (SP).

import os

from app.core.config import settings

BASE_URL = settings.app_base_url


def get_saml_settings():
    return {
        "strict": True,
        "debug": True,
        "sp": {
            "entityId": os.getenv("SAML_ENTITY_ID", BASE_URL),
            "assertionConsumerService": {
                "url": os.getenv("SAML_ACS_URL", f"{BASE_URL}/auth/saml/acs"),
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST",
            },
            "singleLogoutService": {
                "url": f"{BASE_URL}/logout",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
            },
            "x509cert": "",
            "privateKey": "",
        },
        "idp": {
            "entityId": os.getenv("SAML_IDP_ENTITY_ID", ""),
            "singleSignOnService": {
                "url": os.getenv("SAML_IDP_SSO_URL", ""),
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
            },
            "singleLogoutService": {
                "url": os.getenv("SAML_IDP_SLO_URL", ""),
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
            },
            "x509cert": os.getenv("SAML_IDP_CERT", ""),
        },
    }
