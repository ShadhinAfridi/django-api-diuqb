from django.db import models
import datetime


class Departments(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    abbreviation = models.CharField(max_length=255)
    program = models.CharField(max_length=255, default="Undergraduate")
    faculty = models.CharField(max_length=255, null=True, blank=True)
    descriptions = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class MetaData(models.Model):
    lastRefreshTime = models.DateTimeField()
    creationTime = models.DateTimeField()
    lastSignInTime = models.DateTimeField()

class UserDetails(models.Model):
    department = models.ForeignKey(Departments, on_delete=models.PROTECT, default=None, related_name='users', null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    image = models.ImageField(max_length=None, upload_to='user_images/', null=True, blank=True)

class Users(models.Model):
    uid = models.CharField(max_length=255, primary_key=True)
    displayName = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    emailVerified = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)
    metadata = models.ForeignKey(MetaData, on_delete=models.PROTECT, default=None, related_name='user_log')
    details = models.ForeignKey(UserDetails, on_delete=models.PROTECT, default=None, related_name='user_details')

    def __str__(self):
        return self.email

class Courses(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    term = models.CharField(max_length=255, null=True, blank=True)
    department = models.ForeignKey(Departments, on_delete=models.PROTECT, default=None, related_name='courses')

    def __str__(self):
        return "("+self.code+") "+self.name

class Semester(models.Model):
    SHIFT_CHOICES = [('Day', 'Day'), ('Evening', 'Evening')]
    EXAM_CHOICES = [('Midterm', 'Midterm'), ('Final', 'Final')]
    SEMESTER_CHOICES = [('Spring', 'Spring'), ('Summer', 'Summer'), ('Fall', 'Fall')]
    
    shift = models.CharField(max_length=255, choices=SHIFT_CHOICES, default='Day')
    exam = models.CharField(max_length=255, choices=EXAM_CHOICES, default='Midterm')
    semester = models.CharField(max_length=255, choices=SEMESTER_CHOICES, default='Spring')
    year = models.IntegerField(default=datetime.datetime.now().year)

    def __str__(self):
        return f"{self.semester}, {self.exam}, {str(self.year)}, {self.shift}"
    

class Questions(models.Model):
    APPROVAL_CHOICES = [('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')]

    qid = models.CharField(max_length=255, primary_key=True)
    course = models.ForeignKey(Courses, on_delete=models.PROTECT, related_name='questions', blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT, related_name='semesters')
    date = models.DateTimeField()
    approval = models.CharField(max_length=255, choices=APPROVAL_CHOICES, default='Approved')
    filePath = models.TextField()
    uploader = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='uploaded_questions')