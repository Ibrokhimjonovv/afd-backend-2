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
from django.shortcuts import get_object_or_404
from django.http import JsonResponse# Create your views here.

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

# Count
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def increment_count(request, id):
    if request.method == 'POST':
        movie = get_object_or_404(Add_movies, id=id)
        movie.count += 1
        movie.save()
        return JsonResponse({'success': True, 'new_count': movie.count})
    return JsonResponse({'error': 'Invalid request'}, status=400)

class MovieSeriesViewSet(ModelViewSet):
    queryset = MovieSeries.objects.all()
    serializer_class = MovieSeriesSerializer

from rest_framework.decorators import api_view, permission_classes

@api_view(["GET"])
def get_profile(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=401)
    
    serializer = UserModelSerializer(request.user)
    return Response(serializer.data)

from rest_framework.permissions import IsAuthenticated

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_profile(request):
    try:
        user = request.user
        serializer = UserModelSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    

from add_all.models import *

@api_view(['GET'])
def search_films(request):
    query = request.GET.get('query', '')
    if query:
        films = Add_movies.objects.filter(movies_name__icontains=query)
        serializer = AddMoviesSerializer(films, many=True)
        return Response(serializer.data)
    return Response([])

@api_view(['POST'])
def save_film(request):
    if request.method == 'POST' and request.user.is_authenticated:
        film_id = request.data.get('filmId')
        film = get_object_or_404(Add_movies, id=film_id)

        # Foydalanuvchining saqlagan filmlarini yangilash
        user = request.userx    
        if film in user.saved_films.all():
            user.saved_films.remove(film)
        else:
            user.saved_films.add(film)

        user.save()

        # Foydalanuvchining yangi saqlagan filmlarini qaytarish
        saved_films = user.saved_films.all()
        saved_film_ids = [f.id for f in saved_films]
        return Response(saved_film_ids)

    return Response({"error": "Unauthorized"}, status=401)

@api_view(['GET'])
def get_saved_films(request):
    if request.user.is_authenticated:
        saved_films = request.user.saved_films.all()
        saved_film_ids = [f.id for f in saved_films]
        return Response(saved_film_ids)
    return Response({"error": "Unauthorized"}, status=401)