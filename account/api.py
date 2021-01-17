from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .permissions import HasAccess
from .models import User
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    authentication_classes = ([SessionAuthentication, BasicAuthentication])
    permission_classes = [HasAccess]
    queryset = User.objects.all()
    serializer_class = UserSerializer
