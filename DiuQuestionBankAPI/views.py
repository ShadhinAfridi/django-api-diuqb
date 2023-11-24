from rest_framework import generics
from .models import Departments, MetaData, UserDetails, Users, Courses, Semester, Questions
from .serializers import DepartmentsSerializer, MetaDataSerializer, UserDetailsSerializer, UsersSerializer, CoursesSerializer, SemesterSerializer, QuestionsSerializer
from firebase_admin import auth
from django.utils import timezone
from firebase_admin import db
import requests
import base64
from django.core.files.base import ContentFile
from datetime import datetime


class DepartmentsListCreateView(generics.ListCreateAPIView):
    queryset = Departments.objects.all()
    serializer_class = DepartmentsSerializer

class DepartmentsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Departments.objects.all()
    serializer_class = DepartmentsSerializer

class MetaDataListCreateView(generics.ListCreateAPIView):
    queryset = MetaData.objects.all()
    serializer_class = MetaDataSerializer

class MetaDataRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MetaData.objects.all()
    serializer_class = MetaDataSerializer

class UserDetailsListCreateView(generics.ListCreateAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer

class UserDetailsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer

class UsersListCreateView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def fetch_and_store_firebase_users(self):
        # Fetch Firebase users
        page = auth.list_users()
        while page:
            for user_record in page.users:
                # Extract user data from Firebase
                uid = user_record.uid
                display_name = user_record.display_name
                email = user_record.email
                email_verified = user_record.email_verified
                disabled = user_record.disabled
                creation_time = user_record.user_metadata.creation_timestamp
                last_sign_in_time = user_record.user_metadata.last_sign_in_timestamp

                # Convert timestamps to Django DateTimeFields
                creation_datetime = timezone.datetime.fromtimestamp(creation_time / 1000.0, timezone.utc)
                last_sign_in_datetime = timezone.datetime.fromtimestamp(last_sign_in_time / 1000.0, timezone.utc)

                # Create or update MetaData instance
                metadata_data = {
                    'creationTime': creation_datetime,
                    'lastSignInTime': last_sign_in_datetime,
                    'lastRefreshTime': timezone.now(),
                }
                metadata_instance, _ = MetaData.objects.get_or_create(defaults=metadata_data, **metadata_data)

                api_url = 'https://qb.techerax.com/users/about/{}'.format(uid)
                response = requests.get(api_url)

                if response.status_code == 200:
                    user_data = response.json().get('data', {})
                    about = user_data.get('about')
                    department_name = user_data.get('department')
                    department_instance = Departments.objects.filter(name=department_name).first()
                    bitmap_string = user_data.get('image')

                    image = None

                    if not department_instance:
                      department_instance = None

                    if bitmap_string:
                        image_data = base64.b64decode(bitmap_string)
                        image = ContentFile(image_data, name="{}.png".format(uid))
                    
                    details_data = {
                        'department': department_instance,
                        'about': about,
                        'image': image,
                    }
                    details_instance, _ = UserDetails.objects.get_or_create(defaults=details_data, **details_data)

                    # Create or update Users instance
                    user_data = {
                        'uid': uid,
                        'displayName': display_name,
                        'email': email,
                        'emailVerified': email_verified,
                        'disabled': disabled,
                        'metadata': metadata_instance,
                        'details': details_instance,
                    }
                    user_instance, created = Users.objects.get_or_create(defaults=user_data, **{'uid': uid})

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
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

class CoursesListCreateView(generics.ListCreateAPIView):
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer


class CoursesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer

class SemesterListCreateView(generics.ListCreateAPIView):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

class SemesterRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

def parse_date(q_date):
    try:
        # Try parsing the date using the ISO 8601 format
        date_object = datetime.strptime(q_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        # If the ISO format fails, try the original format
        date_object = datetime.strptime(q_date, "%a %b %d %H:%M:%S GMT%z %Y")
    return date_object

class QuestionsListCreateView(generics.ListCreateAPIView):
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer


    def fetch_and_store_fQuestions(self):

        api_url = 'https://qb.techerax.com/questions'
        response = requests.get(api_url)

        if response.status_code == 200:
            api_data = response.json()

            for api_question in api_data.get('data', []):
            # Extract relevant data from API response
                question_id = api_question.get('questionId')
                course_code = api_question.get('code')
                course_name = api_question.get('courseName')
                l_t = api_question.get('lt')
                department_name = api_question.get('departmentName')
                q_shift = api_question.get('shift')
                q_exam = api_question.get('exam')
                q_semester = api_question.get('semester')
                q_year = api_question.get('year')
                uploader_id = api_question.get('uploaderId')
                q_date = api_question.get('date')
                is_approved = api_question.get('isApproved')
                q_link = api_question.get('link')

                #date_object = datetime.strptime(q_date, "%a %b %d %H:%M:%S GMT%z %Y")
                date_object = parse_date(q_date)

                department_instance = Departments.objects.filter(name=department_name).first()
                course_instance = None
                semester_instance = Semester.objects.filter(shift=q_shift, exam=q_exam, semester=q_semester, year=q_year).first()
                users_instance = Users.objects.filter(uid=uploader_id).first()

                if course_name!="Unnamed Courses":
                    course_instance = Courses.objects.filter(name=course_name, department=department_instance).first()
                    

                q_approval = ''

                if is_approved == 0:
                    q_approval = 'Pending'
                if is_approved == 1:
                    q_approval = 'Approved'
                if is_approved == 2:
                    q_approval = 'Rejected'


                questions_data = {
                    "qid": question_id,
                    "date": date_object,
                    "approval": q_approval,
                    "filePath": q_link,
                    "course": course_instance,
                    "semester": semester_instance,
                    "uploader": users_instance
                }

                # print(department_instance)
                # print(course_instance)
                # print(semester_instance)
                # print(users_instance)

                quesition_instance, created = Questions.objects.get_or_create(defaults=questions_data, **{'qid': question_id})

                # Print status
                if created:
                    print(f'Question {question_id} created')
                else:
                    print(f'Question {question_id} not created')
            


class QuestionsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer
