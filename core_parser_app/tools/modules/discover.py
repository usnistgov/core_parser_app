"""Auto discovery of modules
"""
from django.http.request import HttpRequest
import urls
import re
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern
from django.contrib.admindocs.views import simplify_regex
from mongoengine.errors import ValidationError
from core_parser_app.components.module import api as module_api
from core_parser_app.components.module.models import Module
from core_parser_app.tools.modules.exceptions import ModuleError
from core_parser_app.tools.modules.module import AbstractModule


def __assemble_endpoint_data__(pattern, prefix='', filter_path=None):
    """ Creates a dictionary for matched API urls

    :param pattern: the pattern to parse
    :param prefix: the API path prefix (used by recursion)
    :param filter_path:
    :return:
    """
    path = simplify_regex(prefix + pattern.regex.pattern)
    
    if filter_path is not None:
        if re.match('^/?%s(/.*)?$' % re.escape(filter_path), path) is None:
            return None
    
    path = path.replace('<', '{').replace('>', '}')
    
    return {
        'url': path,
        'view': pattern._callback_str,
        'name': pattern.name,        
    }


def __flatten_patterns_tree__(patterns, prefix='', filter_path=None, excluded=list()):
    """ Uses recursion to flatten url tree.

    :param patterns: urlpatterns list
    :param prefix: (optional) Prefix for URL pattern
    :param filter_path:
    :param excluded:
    :return:
    """
    pattern_list = []
    
    for pattern in patterns:
        if isinstance(pattern, RegexURLPattern):
            if pattern.name is not None and pattern.name in excluded: 
                continue
            
            endpoint_data = __assemble_endpoint_data__(pattern, prefix, filter_path=filter_path)
    
            if endpoint_data is None:
                continue
    
            pattern_list.append(endpoint_data)
        elif isinstance(pattern, RegexURLResolver):
            pref = prefix + pattern.regex.pattern
            pattern_list.extend(__flatten_patterns_tree__(
                pattern.url_patterns,
                pref,
                filter_path=filter_path,
                excluded=excluded,
            ))
    
    return pattern_list


def _is_module_managing_occurrences(module):
    """Check if module is managing occurrences

    :param module:
    :return:
    """
    request = HttpRequest()
    request.method = 'GET'

    request.GET = {
        'url': module.url,
        'managing_occurrences': True,
    }

    module_view = AbstractModule.get_view_from_view_path(module.view)

    response = module_view(request).content.decode("utf-8")

    if response == 'false':
        return False
    elif response == 'true':
        return True
    else:
        raise ModuleError("Unexpected value (expected 'true'|'false', got {})".format(response))


def discover_modules():
    """

    :return:
    """
    patterns = __flatten_patterns_tree__(urls.urlpatterns, excluded=urls.excluded)

    # Remove all existing modules
    module_api.delete_all()
    try:
        for pattern in patterns:
            module = Module(url=pattern['url'],
                            name=pattern['name'],
                            view=pattern['view'],
                            multiple=False)
            module.multiple = _is_module_managing_occurrences(module)
            module_api.upsert(module)
    except ValidationError:
        # something went wrong, delete already added modules
        module_api.delete_all()

        error_msg = 'A validation error occurred during the module discovery. ' \
                    'Please provide a name to all modules urls using the name argument.'
        raise ModuleError(error_msg)
    except Exception, e:
        # something went wrong, delete already added modules
        module_api.delete_all()
        raise e
