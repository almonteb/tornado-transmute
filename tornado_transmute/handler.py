import tornado.gen
from functools import wraps
from transmute_core import (
    ParamExtractor, NoArgument,
    default_context, TransmuteFunction
)


def convert_to_handler(context=default_context):

    def decorator(fn):
        transmute_func = TransmuteFunction(fn)

        @tornado.gen.coroutine
        @wraps(transmute_func.raw_func)
        def wrapper(self, *args, **kwargs):
            exc = None
            content_type = self.request.headers.get("Content-Type", None)
            param_extractor = ParamExtractorTornado()
            args, kwargs = param_extractor.extract_params(
                context, transmute_func, content_type
            )
            result = yield transmute_func(*args, **kwargs)
            response = transmute_func.process_result(
                context, result, exc, content_type
            )
            self.set_header("Content-Type", response["content-type"])
            self.set_status(response["code"])
            self.finish(response["body"])
        return wrapper

    return decorator


class ParamExtractorTornado(ParamExtractor):

    def __init__(self, handler_self, path_args, path_kwargs):
        self._handler_self = handler_self
        self._request = handler_self.request
        self._path_args = path_args
        self._path_kwargs = path_kwargs

    @property
    def body(self):
        return self._request.body

    def _query_argument(self, key, is_list):
        qa = self._request.query_argumentns
        if key not in qa:
            return NoArgument
        if is_list:
            return qa[key]
        else:
            return qa[key][0]

    def _header_argument(self, key):
        return self._request.headers.get(key, NoArgument)

    def _path_argument(self, key):
        return self._path_kwargs.get(key, NoArgument)