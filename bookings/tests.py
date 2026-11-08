from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient

from .models import Room, Booking


User = get_user_model()


class BookingAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

        self.room = Room.objects.create(
            room_number="101",
            room_type="Single",
            price_per_night=Decimal("1000.00"),
            is_available=True
        )

        self.client.force_authenticate(user=self.user)
        self.url = reverse('booking-create')

    def test_create_booking_successfully(self):
        response = self.client.post(
            self.url,
            {
                "room": self.room.id,
                "check_in": "2026-11-10",
                "check_out": "2026-11-13"
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(
            Decimal(str(response.data['total_price'])),
            Decimal("3000.00")
        )

    def test_booking_with_invalid_dates(self):
        response = self.client.post(
            self.url,
            {
                "room": self.room.id,
                "check_in": "2026-11-13",
                "check_out": "2026-11-10"
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Booking.objects.count(), 0)
