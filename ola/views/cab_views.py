from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
from rest_framework import generics

from ola.models import BookingHistory, Cab
from ola.serializers.serializer import CabSerializer


class AvailableCabView(generics.ListAPIView):
    queryset = Cab.objects.filter(available=True)
    serializer_class = CabSerializer
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        return self.list(request)


class BookCabView(generics.CreateAPIView):
    serializer_class = BookingHistory
    authentication_classes = (TokenAuthentication,)

    def get_cab(self):
        cabs = Cab.objects.filter(available=True)
        for cab in cabs:
            if cab.status in [Cab.STATUS_RIDING, Cab.STATUS_BOOKED]:
                pass
            else:
                cab.available = False
                cab.save()
                return cab

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class
        data = request.data

        cab = self.get_cab()
        data['cab'] = cab
        serialized_data = serializer(data=data)
        if serialized_data.is_valid():
            serialized_data.save()
            response = {
                'booking': serialized_data.data,
                'cab_details': CabSerializer(cab)
            }
            return Response(response, status=201)

        return Response(serialized_data.errors, status=400)

    def post(self, request):
        return self.create(request)


class RegisterCabView(generics.CreateAPIView):
    serializer_class = CabSerializer
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        return self.create(request)
