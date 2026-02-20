from rest_framework.routers import DefaultRouter
from .views import CategoryView, ItemView

router = DefaultRouter()
router.register(r'categories', CategoryView, basename='category')
router.register(r'items', ItemView, basename='item')

urlpatterns = router.urls

