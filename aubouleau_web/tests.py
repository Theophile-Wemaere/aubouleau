from django.test import TestCase
from django.utils import timezone

from aubouleau_web.models import Building


class BuildingModelTests(TestCase):
    def test_count_floors_returns_actual_number_of_floors(self):
        """
        Building.count_floors() should return the correct number of floors.
        """
        building = Building(name="NDC", picture="", created_at=timezone.now())
        building.save()
        building.floor_set.create(number="0", name="Floor 0", picture="", created_at=timezone.now())
        building.floor_set.create(number="1", name="Floor 1", picture="", created_at=timezone.now())
        building.floor_set.create(number="2", name="Floor 2", picture="", created_at=timezone.now())
        building.floor_set.create(number="3", name="Floor 3", picture="", created_at=timezone.now())

        self.assertEquals(building.count_floors(), 4)

    def test_count_floors_returns_positive_number_of_floors(self):
        """
        Building.count_floors() should return a positive number of floors.
        """
        empty_building = Building(name="Empty", picture="", created_at=timezone.now())
        empty_building.save()
        building = Building(name="NDL", picture="", created_at=timezone.now())
        building.save()
        building.floor_set.create(number="2", name="Floor 0", picture="", created_at=timezone.now())
        building.floor_set.create(number="3", name="Floor 1", picture="", created_at=timezone.now())
        building.floor_set.create(number="4", name="Floor 2", picture="", created_at=timezone.now())

        self.assertGreaterEqual(building.count_floors(), 0)
        self.assertGreaterEqual(empty_building.count_floors(), 0)

    def test_count_rooms_returns_actual_number_of_rooms(self):
        """
        Building.count_rooms() should return the correct number of rooms.
        """
        building = Building(name="NDC", picture="", created_at=timezone.now())
        building.save()
        building.floor_set.create(number="0", name="Floor 0", picture="", created_at=timezone.now())
        building.floor_set.create(number="1", name="Floor 1", picture="", created_at=timezone.now())
        floor_0 = building.floor_set.get(number=0)
        floor_0.room_set.create(number="N01", name="Room N01", seats=30, picture="", created_at=timezone.now())
        floor_0.room_set.create(number="N02", name="Room N02", seats=30, picture="", created_at=timezone.now())
        floor_0.room_set.create(number="N03", name="Room N03", seats=30, picture="", created_at=timezone.now())
        floor_1 = building.floor_set.get(number=1)
        floor_1.room_set.create(number="N10", name="Room N10", seats=30, picture="", created_at=timezone.now())
        floor_1.room_set.create(number="N11", name="Room N11", seats=30, picture="", created_at=timezone.now())

        self.assertEquals(building.count_rooms(), 5)

    def test_count_rooms_returns_positive_number_of_rooms(self):
        """
        Building.count_rooms() should return a positive number of rooms.
        """
        building = Building(name="NDC", picture="", created_at=timezone.now())
        building.save()
        empty_building = Building(name="Empty", picture="", created_at=timezone.now())
        empty_building.save()

        building.floor_set.create(number="0", name="Floor 0", picture="", created_at=timezone.now())
        building.floor_set.create(number="1", name="Floor 1", picture="", created_at=timezone.now())
        floor_0 = building.floor_set.get(number=0)
        floor_0.room_set.create(number="N01", name="Room N01", seats=30, picture="", created_at=timezone.now())
        floor_0.room_set.create(number="N02", name="Room N02", seats=30, picture="", created_at=timezone.now())
        floor_0.room_set.create(number="N03", name="Room N03", seats=30, picture="", created_at=timezone.now())
        floor_1 = building.floor_set.get(number=1)
        floor_1.room_set.create(number="N10", name="Room N10", seats=30, picture="", created_at=timezone.now())
        floor_1.room_set.create(number="N11", name="Room N11", seats=30, picture="", created_at=timezone.now())

        self.assertGreaterEqual(building.count_rooms(), 0)
        self.assertGreaterEqual(empty_building.count_rooms(), 0)
