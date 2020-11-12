from djoser import email


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = 'accounts/reset_password.html'

class EmailResetEmail(email.PasswordResetEmail):
    template_name = 'accounts/reset_email.html'