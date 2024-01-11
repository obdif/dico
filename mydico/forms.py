# from django import forms
# # from .models import CustomUser
# from django.contrib.auth.forms import UserCreationForm
# from .models import UserAccount

# # class EmailLoginForm(forms.Form):
# #     email = forms.EmailField()

# #     def clean_email(self):
# #         email = self.cleaned_data.get('email')
# #         if not CustomUser.objects.filter(email=email).exists():
# #             raise forms.ValidationError('This email is not registered.')
# #         return email

# class Emailsignin(forms.Form):
#     email = forms.EmailField()
    
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
        
#         return email
    
# class Emailsignup(forms.Form):
#     email = forms.EmailField()
    
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
        
#         return email