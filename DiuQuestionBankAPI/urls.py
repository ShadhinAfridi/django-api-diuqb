from django.urls import path
from . import views

urlpatterns = [
    path('departments/', views.DepartmentsListCreateView.as_view(), name='departments-list-create'),
    path('departments/<int:pk>/', views.DepartmentsRetrieveUpdateDestroyView.as_view(), name='departments-retrieve-update-destroy'),

    path('metadata/', views.MetaDataListCreateView.as_view(), name='metadata-list-create'),
    path('metadata/<int:pk>/', views.MetaDataRetrieveUpdateDestroyView.as_view(), name='metadata-retrieve-update-destroy'),

    path('userdetails/', views.UserDetailsListCreateView.as_view(), name='userdetails-list-create'),
    path('userdetails/<int:pk>/', views.UserDetailsRetrieveUpdateDestroyView.as_view(), name='userdetails-retrieve-update-destroy'),

    path('users/', views.UsersListCreateView.as_view(), name='users-list-create'),
    path('users/<int:pk>/', views.UsersRetrieveUpdateDestroyView.as_view(), name='users-retrieve-update-destroy'),

    path('courses/', views.CoursesListCreateView.as_view(), name='courses-list-create'),
    path('courses/<int:pk>/', views.CoursesRetrieveUpdateDestroyView.as_view(), name='courses-retrieve-update-destroy'),

    path('semesters/', views.SemesterListCreateView.as_view(), name='semesters-list-create'),
    path('semesters/<int:pk>/', views.SemesterRetrieveUpdateDestroyView.as_view(), name='semesters-retrieve-update-destroy'),

    path('questions/', views.QuestionsListCreateView.as_view(), name='questions-list-create'),
    path('questions/<int:pk>/', views.QuestionsRetrieveUpdateDestroyView.as_view(), name='questions-retrieve-update-destroy'),
]
