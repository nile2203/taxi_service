from ola.helper.utils import get_or_none
from ola.models import Cab
from ola.serializers.serializer import CabSerializer


class Cabs:
    def __init__(self, latitude=0.0, longitude=0.0, cab_number=None):
        self.latitude = latitude
        self.longitude = longitude
        self.cab_number = cab_number

    @staticmethod
    def check_all_available_cabs():
        cabs = Cab.objects.filter(available=True, service_status=Cab.STATUS_WORKING)
        if not cabs:
            return 0, "No cab is available", None

        return 1, "Cabs are available", cabs

    def find_nearby_cabs_coordinates(self, latitude, longitude, radius):
        latitude_distance = abs(latitude - self.latitude)
        longitude_distance = abs(longitude - self.longitude)

        latitude_distance = latitude_distance ** 2
        longitude_distance = longitude_distance ** 2

        distance = latitude_distance + longitude_distance
        radius = radius ** 2
        if distance <= radius:
            return 1

        return 0

    def get_nearby_available_cabs(self, latitude, longitude, radius):
        nearby_cabs = []
        status, message, available_cabs = Cabs.check_all_available_cabs()
        if not status:
            return 0, message, None

        for cab in available_cabs:
            location = cab.location
            self.latitude = location.latitude
            self.longitude = location.longitude
            result = self.find_nearby_cabs_coordinates(latitude, longitude, radius)
            if result:
                nearby_cabs.append((self.latitude, self.longitude))

        return 1, "", nearby_cabs

    @staticmethod
    def get_serialized_cab(cab, many=False):
        serialized_cabs = CabSerializer.get_serialized(cab, many=many)
        return serialized_cabs

    @staticmethod
    def get_all_serialized_cabs():
        status, message, cabs = Cabs.check_all_available_cabs()
        if not status:
            return 0, message, None

        serialized_cabs = Cabs.get_serialized_cab(cabs, many=True)
        return 1, "", serialized_cabs

    def get_cab_details(self):
        return get_or_none(Cab, cab_number=self.cab_number)
