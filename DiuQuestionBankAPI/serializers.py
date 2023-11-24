from rest_framework import serializers
from .models import Departments, MetaData, UserDetails, Users, Courses, Semester, Questions

class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'

class MetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaData
        fields = '__all__'

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    metadata = MetaDataSerializer()
    details = UserDetailsSerializer()

    class Meta:
        model = Users
        fields = '__all__'

    def create(self, validated_data):
        metadata_data = validated_data.pop('metadata', None)
        details_data = validated_data.pop('details', None)

        # Create a MetaData instance first
        metadata_instance = MetaData.objects.create(**metadata_data)

        # Check if details_data is present before creating UserDetails instance
        if details_data:
            details_instance = UserDetails.objects.create(**details_data)
        else:
            details_instance = None

        # Use the created MetaData and UserDetails instances in the Users creation
        user = Users.objects.create(metadata=metadata_instance, details=details_instance, **validated_data)

        return user
    

class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'