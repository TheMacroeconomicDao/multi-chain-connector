from typing import List

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from api.wallet.models import Wallet
from api.wallet.serializers import WalletSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self) -> List[Wallet]:
        queryset = self.queryset
        user_id = self.request.query_params.get('user_id')

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset

    @extend_schema(
        responses={
            200: {
                'type': 'object', 
                'properties': {
                    'status': {'type': 'string', 'description': 'Status of the operation'},
                    'message': {'type': 'string', 'description': 'Message describing the result'},
                }
            }
        }
    )
    def create(self, request: Request) -> Response:
        """
        This endpoint is responsible for creating a new wallet
        """
        wallet_data = request.data
        serializer = self.get_serializer(data=wallet_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'status': 'success', 'message': 'Wallet saved successfully.'})

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='user_id',
                type=OpenApiTypes.INT,
                description='User ID to filter wallets by user'
            ),
        ],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        This endpoint is responsible for getting a list of user wallets, it is 
        also possible to filter wallets by the 'user_id' parameter
        """
        return super().list(request, *args, **kwargs)
 