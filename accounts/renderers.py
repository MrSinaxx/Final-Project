import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        errors = data.get("errors", None)
        token = data.get("access_token", None)

        if errors is not None:
            return super(UserJSONRenderer, self).render(data)

        if token is not None and isinstance(token, bytes):
            data["access_token"] = token

        return json.dumps({"user": data})


# class TokenJSONRenderer(JSONRenderer):
#     charset = 'utf-8'

#     def render(self, data, accepted_media_type=None, renderer_context=None):

#         errors = data.get('errors', None)
#         access_token = data.get('access_token', None)
#         refresh_token = data.get('refresh_token', None)

#         if errors is not None:
#             return super(TokenJSONRenderer, self).render(data)

#         if access_token is not None and isinstance(access_token, bytes):
#             data['access_token'] = access_token

#         if refresh_token is not None and isinstance(refresh_token, bytes):
#             data['refresh_token'] = refresh_token

#         return json.dumps({'tokens':data})
