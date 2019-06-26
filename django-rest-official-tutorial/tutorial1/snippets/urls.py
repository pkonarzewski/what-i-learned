from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from snippets.views import SnippetViewSet, UserViewSet


router = DefaultRouter()
router.register(r'snippets', SnippetViewSet)
router.register(r'users', UserViewSet)

schema_view = get_schema_view(title='Pastbin API')

urlpatterns = [
    path('schema/', schema_view),
    path('', include(router.urls)),
]
