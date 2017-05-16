"""Core modules forms
"""
from django import forms


class BLOBHostForm(forms.Form):
    """BLOB Host Upload Form
    """

    file = forms.FileField(label='')


class URLForm(forms.Form):
    """BLOB Host URL form
    """
    url = forms.URLField(label='')