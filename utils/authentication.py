import firebase_admin
from firebase_admin import auth
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.utils import timezone

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Extract the Firebase token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            print("Invalid or missing Authorization header")
            return None

        id_token = auth_header.split(' ')[1]

        try:
            # Verify the Firebase token using the 'auth' module
            decoded_token = auth.verify_id_token(id_token)

            # Get or create a Django user based on the UID
            user = self.get_user(decoded_token['uid'])

            # Set the user on the request
            return user, None

        except Exception as e:
            raise AuthenticationFailed(str(e))

    def get_user(self, uid):
        try:
            # Try to get an existing user with the given UID
            user = User.objects.get(username=uid)
            user.last_login = timezone.now()
            user.save()
        except User.DoesNotExist:
            # If the user doesn't exist, create a new user with name, email, and password
            user_data = auth.get_user(uid)  # Fetch additional user data from Firebase
            email = user_data.email
            name = user_data.display_name

            # Set an automated password (you can customize this logic)
            automated_password = User.objects.make_random_password()
            name_parts = name.split()
            # Create the new user
            user = User(
                username=uid,
                email=email,
                first_name = name_parts[0],
                last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else '',
                password=make_password(automated_password),
                last_login = timezone.now()
            )
            user.save()

            # Add the user to the "Students" group
            students_group = Group.objects.get(name='Students')
            user.groups.add(students_group)

        return user

    def authenticate_header(self, request):
        return 'Bearer'
