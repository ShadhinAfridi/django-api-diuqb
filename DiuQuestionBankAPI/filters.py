import django_filters
from .models import Departments, Users, Courses, Semester

class DepartmentsFilter(django_filters.FilterSet):
    class Meta:
        model = Departments
        fields = ['name', 'abbreviation', 'program', 'faculty']

class UsersFilter(django_filters.FilterSet):
    class Meta:
        model = Users
        fields = ['uid', 'department']

class CoursesFilter(django_filters.FilterSet):
    class Meta:
        model = Courses
        fields = ['code', 'name', 'term', 'department']

class SemesterFilter(django_filters.FilterSet):
    class Meta:
        model = Semester
        fields = ['shift', 'exam', 'semester', 'year']