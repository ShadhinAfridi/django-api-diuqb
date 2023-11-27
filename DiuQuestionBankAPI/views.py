from rest_framework import generics
from . import models
from . import serializers
from . import pagination
from . import filters
from django_filters.rest_framework import DjangoFilterBackend
from utils.authentication import FirebaseAuthentication
from rest_framework.permissions import IsAuthenticated
from firebase_admin import auth
import requests
import base64
from django.core.files.base import ContentFile

class DepartmentsListCreateView(generics.ListCreateAPIView):
    queryset = models.Departments.objects.all()
    serializer_class = serializers.DepartmentsSerializer
    pagination_class = pagination.CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.DepartmentsFilter

class DepartmentsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Departments.objects.all()
    serializer_class = serializers.DepartmentsSerializer

class UsersListCreateView(generics.ListCreateAPIView):
    queryset = models.Users.objects.all()
    serializer_class = serializers.UsersSerializer
    pagination_class = pagination.CustomPageNumberPagination
    

    def fetch_and_store_firebase_users(self):
        # Fetch Firebase users
        page = auth.list_users()
        while page:
            for user_record in page.users:
                # Extract user data from Firebase
                uid = user_record.uid

                api_url = 'https://qb.techerax.com/users/about/{}'.format(uid)
                response = requests.get(api_url)

                if response.status_code == 200:
                    user_data = response.json().get('data', {})
                    about = user_data.get('about')
                    department_name = user_data.get('department')
                    department_instance = models.Departments.objects.filter(name=department_name).first()
                    bitmap_string = user_data.get('image')

                    image = None

                    if not department_instance:
                      department_instance = None

                    if bitmap_string:
                        image_data = base64.b64decode(bitmap_string)
                        image = ContentFile(image_data, name="{}.png".format(uid))
                    
                    user_data = {
                        'department': department_instance,
                        'about': about,
                        'image': image,
                    }
                    
                    user_instance, created = models.Users.objects.get_or_create(defaults=user_data, **{'uid': uid})

                    # Print status
                    if created:
                        print(f'User {uid} created')
                    else:
                        print(f'User {uid} updated')

                else:
                    print(f'Error fetching data for user {uid}. Status code: {response.status_code}')
            # Get next batch of users
            page = page.get_next_page()

    def perform_create(self, serializer):
        # Fetch and store Firebase users before creating the serializer instance
        self.fetch_and_store_firebase_users()
        
        # Now, create the serializer instance
        serializer.save()

class UsersRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Users.objects.all()
    serializer_class = serializers.UsersSerializer

class CoursesListCreateView(generics.ListCreateAPIView):
    queryset = models.Courses.objects.all()
    serializer_class = serializers.CoursesSerializer
    pagination_class = pagination.CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.CoursesFilter
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]


class CoursesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Courses.objects.all()
    serializer_class = serializers.CoursesSerializer

class SemesterListCreateView(generics.ListCreateAPIView):
    queryset = models.Semester.objects.all()
    serializer_class = serializers.SemesterSerializer
    pagination_class = pagination.CustomPageNumberPagination

class SemesterRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Semester.objects.all()
    serializer_class = serializers.SemesterSerializer

class QuestionsListCreateView(generics.ListCreateAPIView):
    queryset = models.Questions.objects.all()
    serializer_class = serializers.QuestionsSerializer
    pagination_class = pagination.CustomPageNumberPagination

class QuestionsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Questions.objects.all()
    serializer_class = serializers.QuestionsSerializer
