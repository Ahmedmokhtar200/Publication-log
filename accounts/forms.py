from django import forms


class CustomSignupForm(forms.Form):
    username = forms.CharField(
        label="username",
        max_length=30,
        widget=forms.TextInput(
            attrs={"placeholder": "username", }
        )
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=30,
        widget=forms.TextInput(
            attrs={"placeholder": "First Name", }
        )
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=30,
        widget=forms.TextInput(
            attrs={"placeholder": "Last Name"}
        )
    )
    city = forms.CharField(
        label="City",
        max_length=50,
        widget=forms.TextInput(
            attrs={"placeholder": "City"}
        )
    )
    email = forms.EmailField(
        label="Email",
        max_length=125,
        widget=forms.EmailInput(
            attrs={"placeholder": "Email"}
        )
    )
    password1 = forms.CharField(
        label="Password",
        max_length=1000,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password"}
        )
    )
    password2 = forms.CharField(
        label="Password (again)",
        max_length=1000,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm your password"}
        )

    )


class CustomLogInForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=125,
        widget=forms.EmailInput(
            attrs={"placeholder": "Email"}
        )
    )
    password1 = forms.CharField(
        label="Password",
        max_length=1000,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password"}
        )
    )