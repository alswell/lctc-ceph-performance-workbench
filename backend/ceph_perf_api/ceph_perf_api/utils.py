import json
from django import http

class JSONResponse(http.HttpResponse):

    def __init__(self, data, status=200):
        if status == 204:
            content = ''
        else:
            content = json.dumps(data)
        
        super(JSONResponse, self).__init__(
            status=status,
            content=content,
            content_type='application/json;',
        )

        self.__setitem__('Access-Control-Allow-Headers', "Content-Type, Content-Length, Authorization, Accept, X-Requested-With , yourHeaderFeild")
        self.__setitem__('Access-Control-Allow-Methods', "PUT, POST, GET, DELETE, OPTIONS,PATCH")
        self.__setitem__('Access-Control-Allow-Origin', "*")


def json_response(func):
    def _wrapped(self, request, *args, **kw):
        data = func(self, request, *args, **kw)
        if isinstance(data, http.HttpResponse):
            return data
        elif data is None:
            return JSONResponse('', status=204)
        return JSONResponse(data)
    return _wrapped

