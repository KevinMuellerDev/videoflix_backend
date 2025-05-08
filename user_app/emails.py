from djoser.email import ActivationEmail, PasswordResetEmail

class CustomActivationEmail(ActivationEmail):
    template_name = "djoser/email/activation.html"

class CustomResetPassword(PasswordResetEmail):
    template_name = "djoser/email/resetpassword.html"
