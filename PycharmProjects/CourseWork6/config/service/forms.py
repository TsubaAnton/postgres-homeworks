from django import forms
from crispy_forms.helper import FormHelper
from .models import Client, Message, Newsletter
from crispy_forms.layout import Submit, Layout


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'email',
            'fio',
            'comment',
            Submit('submit', 'Submit', css_class='btn-primary')
        )


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'periodicity',
            'status',
            'message',
            'clients',
            Submit('submit', 'Submit', css_class='btn-primary')
        )


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
