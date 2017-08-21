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

        self.__setitem__('Access-Control-Allow-Headers'
                         , "Content-Type, Content-Length, Authorization, Accept, X-Requested-With , yourHeaderFeild")
        self.__setitem__('Access-Control-Allow-Methods'
                         , "PUT, POST, GET, DELETE, OPTIONS,PATCH")
        self.__setitem__('Access-Control-Allow-Origin'
                         , "*")


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


def parse_filter_param(body):
    filter_param = {}
    for key, value in body.items():
        if isinstance(value, dict):
            for k, v in value.items():
                filter_param[key + '__' + k] = v
        else:
            filter_param[key] = value
    return filter_param


class ForeignKeyConvert(object):
    def __init__(self, foreign_key):
        self.foreign_key = foreign_key

    def __call__(self, *args, **kwargs):
        return self.foreign_key


def query_to_dict(obj, foreign_convert=None):
    if isinstance(obj, QuerySet):
        data = json.loads(serializers.serialize("json", obj))
        for i in range(len(data)):
            pk = data[i]['pk']
            data[i] = data[i]["fields"]
            data[i]['id'] = pk
            if foreign_convert:
                data[i][foreign_convert.foreign_key] = foreign_convert(obj[i])
        return data

    if isinstance(obj, Model):
        data = json.loads(serializers.serialize("json", [obj]))
        if len(data) == 0:
            return None
        return [data[0]["fields"]]
