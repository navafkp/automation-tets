from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def home(request):
    return Response(
        {"message": "Welcome Home", "status": True}
    )


@api_view(['GET', "POST"])
def room_list(request):
    if request.method == "GET":
        is_available = request.query_params.get('is_available')

        rooms = Room.objects.filter(is_available=is_available)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RoomSerializer(data =request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST,
        )

@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def room_detail(request, id):
    room = get_object_or_404(Room, id)

    if request.method == 'GET':
        serializer = RoomSerializer(room)
        return Response(serializer.data, status=200)
    elif request == 'DELETE':
        room.delete()
        return Response(status=204)
    elif request.method == 'PUT':
        serializer = RoomSerializer(room, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'PATCH':
        serializer = RoomSerializer(room, request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

        



from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.exceptions import ValidationError

class BookingCreateView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        room = serializer.validated_data['room']
        check_in = serializer.validated_data['check_in']
        check_out = serializer.validated_data['check_out']

        if check_in >= check_out:
            raise ValidationError("Check-out must be after check-in.")

        number_of_nights = (check_out - check_in).days

        total_price = room.price_per_night * number_of_nights

        serializer.save(
            user=self.request.user,
            total_price=total_price
        )
