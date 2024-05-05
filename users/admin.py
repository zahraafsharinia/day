from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import CustomUser
from jalali_date.fields import SplitJalaliDateTimeField
from jalali_date.widgets import AdminSplitJalaliDateTime


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['last_login'] = SplitJalaliDateTimeField(label='date time', widget=AdminSplitJalaliDateTime)

    class Meta:
        model = CustomUser
        fields = ["national_number", "first_name", "last_name", "personnel_code", "branch_code", "organization_code",
                  "organization_name", "sub_organization_name", "post_code", "post_name", "post_level_code",
                  "post_level_name", "status_name"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="Enter the new password <a href = \"../password/\">here</a>")

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['last_login'] = SplitJalaliDateTimeField(label='date time', widget=AdminSplitJalaliDateTime)
    # class Meta:
    #     model = CustomUser
    #     fields = ["national_number", "password", "first_name", "last_name", "personnel_code", "branch_code", "organization_code",
    #               "organization_name", "sub_organization_name", "post_code", "post_name", "post_level_code",
    #               "post_level_name", "status_name"]


class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["username", "national_number", "first_name", "last_name", "personnel_code", "branch_code",
                    "organization_code", "organization_name", "sub_organization_name", "post_code", "post_name",
                    "post_level_code", "post_level_name", "status_name"]
    list_filter = ["is_staff"]
    fieldsets = [
        (None, {"fields": ["username", "password"]}),
        ("Personal info", {"fields": ["email", "national_number", "first_name", "last_name", "personnel_code", "branch_code",
                                      "organization_code", "organization_name", "sub_organization_name", "post_code",
                                      "post_name", "post_level_code", "post_level_name", "status_name"]}),
        ("Permissions", {"fields": ["is_staff", "is_superuser", "last_login"]}),
    ]
    add_fieldsets = [
        (None, {"classes": ["wide"],
                "fields": ["username", "password1", "password2"]}),
    ]
    search_fields = ["national_number"]
    ordering = ["national_number"]
    filter_horizontal = []


admin.site.unregister(Group)
admin.site.register(CustomUser, UserAdmin)