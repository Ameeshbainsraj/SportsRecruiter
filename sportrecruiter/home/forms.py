from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import HomeTeam, Tryout  # Assuming you need these for other forms
from .models import CustomUser

# Get the custom user model
CustomUser = get_user_model()

# User Creation Form
class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.RadioSelect,
        initial='PLAYER'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')

# Custom Authentication Form
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)

# Team Profile Form (assuming you need this somewhere)
class TeamProfileForm(forms.ModelForm):
    class Meta:
        model = HomeTeam
        fields = ['team_name', 'team_logo', 'team_bio', 'team_region']

# Tryout Form (assuming you need this somewhere)
class TryoutForm(forms.ModelForm):
    class Meta:
        model = Tryout
        fields = ['title', 'date', 'description', 'is_active']

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES, 
        widget=forms.RadioSelect,
        initial='PLAYER'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=254, label='Email or Username')
    password = forms.CharField(widget=forms.PasswordInput)




class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'bio', 'profile_picture']
