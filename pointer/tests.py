import csv
import random
from collections import defaultdict

from django.test import TestCase

# Create your tests here.


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
