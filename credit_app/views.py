from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate, get_user_model

from .models import Buyer_credit, Item_purchased, Item
from .serializers import (
    UsercreditSerializer, 
    ItemPurchasedSerializer, 
    UserSerializer, 
    LoginSerializer, 
    RegisterSerializer,
    ItemSerializer
)

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@swagger_auto_schema(
    security=[{'Bearer': []}]
)


class Show_buyers(viewsets.ModelViewSet):
    queryset = Buyer_credit.objects.all()
    serializer_class = UsercreditSerializer


class show_item_purchased(viewsets.ModelViewSet):
    queryset = Item_purchased.objects.all()
    serializer_class = ItemPurchasedSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(security=[{'Bearer': []}])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        user = self.request.user
        item_purchased = serializer.save(buyer=user)
        price = item_purchased.item.price
        
        credit_obj, created = Buyer_credit.objects.get_or_create(buyer=user, defaults={'credit_amount': 300})

        # Deduct price from credit_amount
        credit_obj.credit_amount -= price
        credit_obj.save()


class ItemViewset(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class =  ItemSerializer


class Show_UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Buyer_credit.objects.create(buyer=user, credit_amount=300)
            tokens = get_tokens_for_user(user)

            return Response({
                "user": UserSerializer(user).data,
                "tokens": tokens,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                tokens = get_tokens_for_user(user)
                return Response({
                    'user': UserSerializer(user).data,
                    'tokens': tokens,
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


class ProtectedView(APIView):
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    

    @swagger_auto_schema(security=[{'Bearer': []}])
    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}!"})



class TokenRefreshView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)
            return Response({"access": new_access_token}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
