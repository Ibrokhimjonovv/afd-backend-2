from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('users', UserViewSet)
router.register("departments", DepartmentsViewSet)
router.register("movies", AddMoviesViewSet)
router.register("swiper-films", AddSwiperFilmsSet)
router.register('series', MovieSeriesViewSet, basename='series')

urlpatterns = [
    path("", include(router.urls)),
    path("get_profile/", get_profile),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('movies/search/', search_films, name='search_films'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('films/<int:id>/increment/', IncrementFilmCountView.as_view(), name='increment-film-count'),
]