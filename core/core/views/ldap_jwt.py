import json
import requests
import os

from rest_framework import exceptions

from rest_framework_jwt.views import (
    JSONWebTokenAPIView
)
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer
)
from rest_framework_jwt.settings import (
    api_settings
)

from rest_framework_jwt.authentication import (
    JSONWebTokenAuthentication
)

from core.utils.utils import (
    authenticate_ldap,
    search_user
)

from django.utils.translation import ugettext as _
from rest_framework import serializers

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class JSONWebTokenLDAPAuthentication(JSONWebTokenAuthentication):
    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        user = search_user(username)

        if user is None:
            msg = _('Invalid signature (Empty User).')
            raise exceptions.AuthenticationFailed(msg)

        return user


class JSONWebTokenLDAPSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate_ldap(**credentials)
            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


class ObtainJSONWebTokenLDAP(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.
    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = JSONWebTokenLDAPSerializer


obtain_ldap_jwt_token = ObtainJSONWebTokenLDAP.as_view()
