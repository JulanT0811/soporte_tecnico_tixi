# soporte_tecnico/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from soporte_tecnico.views.health import health_check
from soporte_tecnico.views.category import CategoryViewSet
from soporte_tecnico.views.priority import PriorityViewSet
from soporte_tecnico.views.ticket import TicketViewSet, CommentViewSet, AttachmentViewSet
from soporte_tecnico.views.user import UserViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'priorities', PriorityViewSet, basename='priority')
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'attachments', AttachmentViewSet, basename='attachment')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Auth endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', TokenBlacklistView.as_view(), name='logout'),
    path('auth/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    
    # Health check
    path('health/', health_check),
    
    # Router endpoints
    path('', include(router.urls)),
]