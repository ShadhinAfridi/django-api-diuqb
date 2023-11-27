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
