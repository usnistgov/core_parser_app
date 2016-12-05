"""Views
"""

from core_parser_app.tools.modules.builtin.models import AutoKeyModule
from models import PositiveIntegerInputModule, ExampleAutoCompleteModule, ChemicalElementMappingModule, \
    CountriesModule, FlagModule, ChemicalElementCheckboxesModule


def positive_integer(request):
    return PositiveIntegerInputModule().render(request)


def example_autocomplete(request):
    return ExampleAutoCompleteModule().render(request)


def chemical_element_mapping(request):
    return ChemicalElementMappingModule().render(request)


def countries(request):
    return CountriesModule().render(request)


def flag(request):
    return FlagModule().render(request)


def chemical_element_selection(request):
    return ChemicalElementCheckboxesModule().render(request)


def auto_key_randint(request):
    return AutoKeyModule(generateKey_int).render(request)


def generateKey_int(values):
    from random import randint
    key = randint(0, 1000)
    while key in values:
        key = randint(0, 1000)
    return key


def auto_key_randstr(request):
    return AutoKeyModule(generateKey_str).render(request)


def generateKey_str(values):
    import random
    import string
    N = 10
    key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    while key in values:
        key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    return key


def auto_key_int_sequence(request):
    return AutoKeyModule(generateKey_int_sequence).render(request)


def generateKey_int_sequence(values):
    if len(values) == 0:
        return 1
    else:
        value_max = max(values)
        return int(value_max) + 1
