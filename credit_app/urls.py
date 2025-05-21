from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Show_buyers, show_item_purchased, Show_UserViewSet, RegisterView, LoginView, LogoutView, ProtectedView , ItemViewset

router = DefaultRouter()
router.register(r'buyercredits', Show_buyers) # r is used to escape the newline 
router.register(r'items_purchase', show_item_purchased)  
router.register(r'users', Show_UserViewSet) 
router.register(r'items', ItemViewset) 
urlpatterns = [
   
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name= 'register'),
    path('login/', LoginView.as_view(), name= 'login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
]
