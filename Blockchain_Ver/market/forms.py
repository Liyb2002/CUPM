from django import forms
from django.contrib.auth.models import User
from .models import Profile, Comment

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date', 'website', 'address')


from django.core.validators import MaxValueValidator, MinValueValidator

class ActionForm(forms.Form):
    amount = forms.DecimalField(min_value=0) # # of shares
    estimate_low = forms.DecimalField(label='Estimated Lower Bound', min_value=0, max_value=1)
    estimate_high = forms.DecimalField(label='Estimated Higher Bound', min_value=0, max_value=1)
    option = forms.ChoiceField(label='Option', choices=[('Buy', 'Buy'), ('Sell', 'Sell')])


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )