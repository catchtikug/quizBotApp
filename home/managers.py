from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as __

class UsersManager(BaseUserManager):
    def create_superuser(self, email, username, user_agreement_accepted, country, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        return self.create_user(email, username, user_agreement_accepted, country, password, **other_fields)
        

    def create_user(self, email, username, user_agreement_accepted, country, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, user_agreement_accepted=user_agreement_accepted, country=country, **other_fields)
        user.set_password(password)
        user.save()
        return user