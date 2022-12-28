from django.contrib.auth.models import BaseUserManager
from phone_field import PhoneNumber

class UserManager(BaseUserManager):
    """Управляет созданием пользователя."""

    def create_user(self, first_name, last_name,
            email, agreement, phone_number, password=None,
            ):
        if not first_name:
            raise ValueError('Users Must Have An first_name')
        if not last_name:
            raise ValueError('Users Must Have An last_name')
        if not email:
            raise ValueError('Users Must Have An Email Address')
        if not phone_number:
            raise ValueError('Users Must Have A Phone Number')
        if agreement != True:
            raise ValueError('Give me your agreement, stuped bastard!')
        user = self.model(
            username=email,
            email=self.normalize_email(email),
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            agreement=agreement

        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # def create_super_user(self, username, email, password=None):

    #     if not email:
    #         raise ValueError('Users Must Have An Email Address')
    #     user = self.model(
    #         username=username,
    #         email=self.normalize_email(email),
    #     )
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    # def create_superuser(self, username, email, password=None):
    #     user = self.create_super_user(
    #         username=username,
    #         email=email,
    #         password=password,
    #     )
    #     user.is_admin = True
    #     user.is_staff = True
    #     user.is_superuser = True
    #     user.save(using=self._db)
    #     return user
