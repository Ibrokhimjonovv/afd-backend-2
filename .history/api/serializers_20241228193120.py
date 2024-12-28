from rest_framework.serializers import ModelSerializer, ReadOnlyField
from users.models import User
from add_all.models import *
from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        uname = data.get('username')
        print("Username:", uname)
        pword = data.get('password')
        print("Password:", pword)

        if uname and pword:
            user = User.objects.get(username=uname)
            if user.check_password(pword):
                
                print("Authentication successful")
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                return data
            else:
                print("Authentication failed")
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

from rest_framework import serializers
from users.models import User

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            firstName = validated_data["firstName"],
            lastName = validated_data["lastName"],
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # Parolni hash qiladi
        user.save()
        return user
    

class UserModelSerializer(serializers.ModelSerializer):
    # Foydalanuvchi modelida bo'lishi kerak bo'lgan maydonlarni qo'shing
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    dateJoined = serializers.DateTimeField(source='date_joined')

    class Meta:
        model = User
        fields = "__all__"

class DepartmentsSerializer(ModelSerializer):
    class Meta:
        model = Add_departments
        fields = "__all__"


class MovieSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSeries
        fields = "__all__"


class AddMoviesSerializer(ModelSerializer):
    series = MovieSeriesSerializer(many=True, read_only=True)

    class Meta:
        model = Add_movies
        fields = "__all__"
