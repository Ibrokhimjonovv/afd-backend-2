from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from .serializers import *
from users.models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer
from add_all.models import *
from add_all.models import *
from users.models import User
# Create your views here.

class LoginView(APIView):
    authentication_classes = [BasicAuthentication]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Yangi foydalanuvchini yaratish
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(ModelViewSet):
    authentication_classes = [BasicAuthentication]
    serializer_class = UserModelSerializer
    queryset = User.objects

class DepartmentsViewSet(ModelViewSet):
    authentication_classes = [BasicAuthentication]
    serializer_class = DepartmentsSerializer
    queryset = Add_departments.objects

class AddMoviesViewSet(ModelViewSet):
    authentication_classes = [BasicAuthentication]
    serializer_class = AddMoviesSerializer
    queryset = Add_movies.objects

class MovieSeriesViewSet(ModelViewSet):
    queryset = MovieSeries.objects.all()
    serializer_class = MovieSeriesSerializer

class AddSwiperFilmsSet(ModelViewSet):
    authentication_classes = [BasicAuthentication]
    serializer_class = AddSwiperFilmsSerializer
    queryset = SwiperFilms.objects


# from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import viewsets

# class ProfileViewSet(ModelViewSet):
#     serializer_class = UserModelSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         print(User.objects.filter(user=user))
#         return User.objects.filter(user=user)

#     @action(detail=False, methods=['get'])
#     def current(self, request):
#         user = request.user
#         profile = User.objects.get(user=user)
#         serializer = self.get_serializer(profile)
#         return Response(serializer.data)
from rest_framework.decorators import api_view, authentication_classes

@api_view(["GET"])
def get_profile(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=401)
    
    serializer = UserModelSerializer(request.user)
    return Response(serializer.data)
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_profile(request):
#     user = request.user
#     serializer = UserModelSerializer(user)
#     return Response(serializer.data)