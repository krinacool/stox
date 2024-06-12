from django import forms
from .models import Upstox

class UpstoxForm(forms.ModelForm):
    class Meta:
        model = Upstox
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['redirect_url'].widget.attrs['readonly'] = True

    class Media:
        js = ('admin/js/upstox_admin.js',)
