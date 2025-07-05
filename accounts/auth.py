from rest_framework.exceptions import AuthenticationFailed, APIException

from django.contrib.auth.hashers import check_password, make_password

from accounts.models import User
from companies.models import Enterprise, Employee


class Authentication:
    def signin(self, email=None, password=None) -> User:
        exception_auth = AuthenticationFailed('E-mail and/or password incorrect(s)')

        user_exists = User.objects.filter(email=email).exists()

        if not user_exists:
            raise exception_auth

        user = User.objects.filter(email=email).first()

        if not check_password(password, user.password):
            raise exception_auth

        return user

    def signup(self, name, email, password, type_account='owner', company_id=False):
        if not name or name == '':
            raise APIException('Name must not be null')

        if not email or email == '':
            raise APIException('E-mail must not be null')

        if not password or password == '':
            raise APIException('Password must not be null')

        if type_account == 'employee' and not company_id:
            raise APIException('Company id must not be null')

        user = User
        if user.objects.filter(email=email).exists():
            raise APIException('This email already exists on the platform')

        password_hashed = make_password(password)

        created_user = user.objects.create(
            name=name,
            email=email,
            password=password_hashed,
            is_owner=0 if type_account == 'employee' else 1
        )

        if type_account == 'owner':
            created_enterprise = Enterprise.objects.create(
                name='New Company name',
                user_id=created_user.id
            )

        if type_account == 'employee':
            Employee.objects.create(
                enterprise_id=company_id or created_enterprise.id,
                user_id=created_user.id
            )

        return created_user