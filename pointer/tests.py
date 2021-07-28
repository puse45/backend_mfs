import csv
import json
import random
from collections import defaultdict

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

# Create your tests here.
from pointer.models import ClosestPointCompute


def test_case(length: int = 10000):
    lst1 = [random.randint(-(10 ** 9), 10 ** 9) for i in range(length)]
    lst2 = [random.randint(-(10 ** 9), 10 ** 9) for i in range(length)]
    return lst1, lst2


def test_case2(path):
    columns = defaultdict(list)  # each value in each column is appended to a list

    with open(path) as f:
        reader = csv.DictReader(f)  # read rows into a dictionary format
        for row in reader:  # read a row as {column1: value1, column2: value2,...}
            for (k, v) in row.items():  # go over each column name and value
                columns[k].append(v)  # append the value into the appropriate list

    return columns["lat"], columns["lng"]


# models test
class ClosestPointComputeTest(TestCase):
    points = [[2.5, 3.1], [1.6, 1.999], [5, 4], [5, 4]]

    def create_closest_point_compute(self, points):
        return ClosestPointCompute.objects.create(points=points)

    def test_closest_point_creation(self):
        cpc = self.create_closest_point_compute()
        self.assertTrue(isinstance(cpc, ClosestPointCompute))
        self.assertEqual(cpc.points, self.points)


# views test
class ViewsClosestPointComputeTestCase(TestCase):
    def test_closest_point_compute(self):
        """Closest point compute"""
        response = self.client.get("http://localhost:8000/api/points/")
        self.assertEqual(response.status_code, 200)


# api test
class ViewsClosestPointComputePostTestCase(APITestCase):
    def test_closest_point_compute_create(self):
        """Closest point compute create"""
        payload = {"points": [[2.5, 3.1], [1.6, 1.999], [5, 4], [5, 4]]}
        expected_result = {
            "point A": [5, 4],
            "point B": [5, 4],
            "distance between": 0.0,
        }
        response = self.client.post("/api/points/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ClosestPointCompute.objects.count(), 1)
        self.assertEqual(ClosestPointCompute.objects.get().points, payload["points"])
        self.assertEqual(ClosestPointCompute.objects.get().result, expected_result)
