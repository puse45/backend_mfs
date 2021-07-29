import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from pointer.models import ClosestPointCompute

# Create your tests here.


# models test
class ClosestPointComputeTest(TestCase):
    points = [[2.5, 3.1], [1.6, 1.999], [5, 4], [5, 4]]

    def create_closest_point_compute(self, points):
        return ClosestPointCompute.objects.create(points=points)

    def test_closest_point_creation(self):
        cpc = self.create_closest_point_compute(points=self.points)
        self.assertTrue(isinstance(cpc, ClosestPointCompute))
        self.assertEqual(cpc.points, self.points)


# views test
class ViewsClosestPointComputeTestCase(TestCase):
    def test_closest_point_compute(self):
        """Closest point compute"""
        response = self.client.get("/api/points/")
        self.assertEqual(response.status_code, 200)


# api test
class ViewsClosestPointComputePostTestCase(APITestCase):
    def test_closest_point_compute_create(self):
        """Closest point compute create"""
        payload = {"points": [[2.5, 3.1], [1.6, 1.999], [5, 4], [5, 4]]}
        expected_result = {"point A": [5.0, 4.0], "point B": [5.0, 4.0]}

        response = self.client.post("/api/points/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ClosestPointCompute.objects.count(), 1)
        self.assertEqual(ClosestPointCompute.objects.get().points, payload["points"])
        self.assertEqual(
            ClosestPointCompute.objects.get().result.get("closest points"),
            expected_result,
        )
