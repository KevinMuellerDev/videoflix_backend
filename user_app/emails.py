from djoser.email import ActivationEmail

class CustomActivationEmail(ActivationEmail):
    template_name = "djoser/email/activation.html"
