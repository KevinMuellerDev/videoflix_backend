from djoser.email import ActivationEmail, PasswordResetEmail
from user_app.emails import CustomActivationEmail, CustomResetPassword


def test_custom_activation_email_inherits():
    email = CustomActivationEmail()
    assert isinstance(email, ActivationEmail)
    assert email.template_name == "djoser/email/activation.html"


def test_custom_reset_password_email_inherits():
    email = CustomResetPassword()
    assert isinstance(email, PasswordResetEmail)
    assert email.template_name == "djoser/email/resetpassword.html"