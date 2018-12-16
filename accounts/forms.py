from django import forms
from .models import UserManager
from django.core.exceptions import ObjectDoesNotExist


class SignUpForm(forms.ModelForm):
    """User Signup Form"""
    class Meta:
        #Use UserManager class from model.py
        model = UserManager
        #Prepare the same fields as being made in model.py
        fields = ('username', 'first_name', 'last_name', 'phone', 'restaurant', 'password', )
        #パスワードform作るときのおまじない
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': '*Password'}),
        }

    #Create Password Confirmation form
    password2 = forms.CharField(
        label='checking password',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': '*Confirm Password'}),
    )

    #Create Input form
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'placeholder': '*Username'}
        self.fields['first_name'].widget.attrs = {'placeholder': '*First name'}
        self.fields['first_name'].required = True
        self.fields['last_name'].widget.attrs = {'placeholder': '*Last name'}
        self.fields['last_name'].required = True
        self.fields['phone'].widget.attrs = {'placeholder': '*Phone'}
        self.fields['phone'].required = True
        self.fields['restaurant'].widget.attrs = {'placeholder': '*Restaurant name'}
        self.fields['restaurant'].required = True

    # def clean_firstName(self):
    #     firstName = self.clean_data['first_name']
    #     return firstName
    #
    # def clean_lastName(self):
    #     lastName = self.clean_data['last_name']
    #     return lastName
    #
    # def clean_restaurant(self):
    #     restaurant = self.clean_data['restanrant']
    #     return restaurant

    def clean_username(self):
        """validate phone"""
        username = self.cleaned_data['username']

        #if phone is less than 9 letters, show error message
        if len(username) < 3:
            raise forms.ValidationError('username must be more than 3 letters')
        #if phoen is not numeric, show error message
        if username.isnumeric():
            raise forms.ValidationError('username must not be only numbers')
        return username

    def clean(self):
        """validate password and confirm password"""
        super(SignUpForm, self).clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        #if password and confirm password dont match, show error message
        if password != password2:
            raise forms.ValidationError("password and confirmed password don't match")

    def save(self, commit=True):
        """hash password and save user info"""

        user_info = super(SignUpForm, self).save(commit=False)
        user_info.set_password(self.cleaned_data["password"])
        if commit:
            user_info.save()
            # UserManager.objects.create(user=user_info)

        return user_info


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username Number',
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Username Number',
                                      'autofocus': True})
    )
    """
    - render_value=True... when user go back to login page, password remains
    - strip=Flase...When strip=True, remove space in the first and last place
    """
    password = forms.CharField(
        label='password',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder':'Password'}, render_value=True)
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        #create object to keep the user info
        self.user_request_to_login = None

    def clean_password(self):
        """validate password"""
        password = self.cleaned_data['password']
        return password

    def clean_username(self):
        """validate username number"""
        username = self.cleaned_data['username']
        return username

    def clean(self):
        """validate username and its password are corresponding"""
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        try:
            requesting_user = UserManager.objects.get(username=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError('Input correct username')
        if not requesting_user.check_password(password):
            raise forms.ValidationError('Input correct password')
        self.user_request_to_login = requesting_user


    def get_login_user(self):
        """return user id which has corresponding username and database id"""
        return self.user_request_to_login