from django.contrib.auth.forms import PasswordChangeForm

from .models import Principal, Membership
from django.forms import ModelForm, CharField, PasswordInput


class PrincipalForm(ModelForm):
    class Meta:
        model = Principal
        fields = ['group', 'limit_rest_time', 'limit_food_time', 'limit_number_of_rest_number',
                  'limit_number_of_food_number', 'duration']


class MembershipForm(ModelForm):
    class Meta:
        model = Membership
        fields = ['user', 'group']


class PasswordChangeCustomForm(PasswordChangeForm):
    error_css_class = 'has-error'
    error_messages = {'password_incorrect':
                          "Το "}
    old_password = CharField(required=True, label='Old Password',
                             widget=PasswordInput(attrs={
                                 'class': 'form-control'}),
                             error_messages={
                                 'required': 'Το '})

    new_password1 = CharField(required=True, label='new password',
                              widget=PasswordInput(attrs={
                                  'class': 'form-control'}),
                              error_messages={
                                  'required': 'Το '})
    new_password2 = CharField(required=True, label='new password',
                              widget=PasswordInput(attrs={
                                  'class': 'form-control'}),
                              error_messages={
                                  'required': 'Το'})
