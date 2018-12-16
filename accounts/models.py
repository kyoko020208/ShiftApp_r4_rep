from django.db import models
from django.contrib.auth.models import AbstractUser

# class UserManager(BaseUserManager):
#     def create_user(self, phone, first_name, last_name, password, restaurant):
#         """
#         Create users
#         :param first_name: First name
#         :param last_name: Last name
#         :param phone: Mobile phone number
#         :param password: Password
#         :return: AuthUser object
#         """
#
#         if not phone:
#             raise ValueError('phone is required')
#
#         if not first_name:
#             raise ValueError('First Name is required')
#
#         if not last_name:
#             raise ValueError('Last Name is required')
#
#         if not password:
#             raise ValueError('Password is required')
#
#
#         user = self.model(phone=phone,
#                           first_name=first_name,
#                           last_name=last_name,
#                           password=password,
#                           restaurant=restaurant)
#
#         user.is_active =True
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#
#     def create_superuser(self, phone, first_name, last_name, password, restaurant):
#         """
#         create super user
#         """
#         user = self.create_user(phone=phone,
#                           first_name=first_name,
#                           last_name=last_name,
#                           password=password,
#                           restaurant=restaurant)
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user



class UserManager(AbstractUser):
    """
    Manage User Info
    """
    class Meta:
       db_table = 'AuthUser'

    # def get_full_name(self):
    #     """
    #     Get user's full name
    #     :return: first_name + last_name
    #     """
    #     return self.last_name + self.first_name

    user_id = models.AutoField(primary_key=True, unique=True)

    username = models.CharField(max_length=255, unique=True)

    first_name = models.CharField(verbose_name='first name', max_length=30)

    last_name = models.CharField(verbose_name='last name', max_length=30)

    phone = models.CharField(verbose_name='Phone Number', max_length=15, unique=True)

    password = models.CharField(verbose_name='password', max_length=128)

    restaurant = models.CharField(verbose_name='restaurant', max_length=50)

    date_joined = models.DateTimeField(auto_now_add=True)

    #Check if he already exists in the list
    is_staff = models.BooleanField(
        verbose_name='staff status',
        default=False,
    )


    #Check if he is a manager
    is_manager = models.BooleanField(
        verbose_name='manager status',
        default=False,
    )

    # Check if the account is active
    is_active = models.BooleanField(
        verbose_name='active',
        default=True,
    )

    # PHONE_FIELD = 'phone'
    # USERNAME_FIELD = 'phone'
    # REQUIRED_FIELDS = ['first_name', 'last_name', 'restaurant']
    #
    # objects = AuthUserManager()

    def __str__(self):
        return self.username