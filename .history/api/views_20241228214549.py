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

# Saqlangan filmlarni olish uchun API
class SavedFilmsView(APIView):
    permission_classes = [IsAuthenticated]  # Foydalanuvchi tizimga kirgan bo'lishi kerak

    # Saqlangan filmlar ro'yxatini olish
    def get(self, request):
        saved_films = SavedFilm.objects.filter(user=request.user)  # Foydalanuvchining saqlagan filmlari
        serializer = SavedFilmSerializer(saved_films, many=True)  # Serializer orqali JSON formatiga o'tkazish
        return Response(serializer.data)

    # Filmni saqlash
    def post(self, request):
        film_id = request.data.get('filmId')  # POST orqali yuborilgan film ID sini olish

        if not film_id:
            return Response({"detail": "Film ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            film = Add.objects.get(id=film_id)  # Filmni topish
        except Film.DoesNotExist:
            return Response({"detail": "Film not found."}, status=status.HTTP_404_NOT_FOUND)

        # Filmni foydalanuvchi tomonidan saqlash
        saved_film, created = SavedFilm.objects.get_or_create(user=request.user, film=film)

        # Saqlangan filmlar ro'yxatini qaytarish
        saved_films = SavedFilm.objects.filter(user=request.user)
        serializer = SavedFilmSerializer(saved_films, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)