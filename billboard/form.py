from django.forms import ModelForm
from .models import Message, Configuration


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['group_message', 'category', 'configuration', 'content', 'image']


class ConfigurationForm(ModelForm):
    class Meta:
        model = Configuration
        fields = ['font_size', 'color', 'text_align', 'background_color']
