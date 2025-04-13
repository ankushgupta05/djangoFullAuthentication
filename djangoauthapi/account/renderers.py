from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''         
        if 'ErrorDetail' in str(data):  # if ErrorDetail word present in data then that data is a error like {'email': [ErrorDetail(string='user with this Email  already exists.', code='unique')]}
            response = json.dumps({'errors':data})
        else:
            response = json.dumps(data)

        return response  # if everything is right then good and send data as a response