import json
from django import http
from django.db.models.query import QuerySet
from django.db.models import Model
from django.core import serializers

class JSONResponse(http.HttpResponse):

    def __init__(self, data, status=200):
        if status == 204:
            content = ''
	elif isinstance(data, QuerySet):
	    content = serializers.serialize("json", data)
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
        request.DATA = None
        if request.body:
            try:
                request.DATA = json.loads(request.body)
            except (TypeError, ValueError) as e:
                return JSONResponse('malformed JSON request: %s' % e, 400)

        data = func(self, request, *args, **kw)
        if isinstance(data, http.HttpResponse):
            return data
        elif data is None:
            return JSONResponse('', status=204)
        return JSONResponse(data)
    return _wrapped

def query_to_dict(obj):
    if isinstance(obj, QuerySet):
    	data = json.loads(serializers.serialize("json", obj))
	for i in range(len(data)):
	    data[i] = data[i]["fields"]
        return data

    if isinstance(obj, Model):
    	data = json.loads(serializers.serialize("json", [obj]))
	if len(data) == 0:
	    return None
	return [data[0]["fields"]]
    
