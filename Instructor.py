"""
@author Margie Lehmann
This file contains the Instructor class for out Univeristy data tracking program.
"""

from collections import defaultdict
from typing import Tuple, DefaultDict, Iterator, List


class Instructor:
    """ Class to hold instructor data """
    prettytable_header: List[str] = [
        'CWID', 'Name', 'Dept', 'Course', 'Students']

    def __init__(self, cwid: str, name: str, department: str) -> None:
        """ Method to initialize a Student """
        self._cwid: str = cwid
        self._name: str = name
        self._department: str = department
        # Course to number of Students
        self._courses: DefaultDict[str, int] = defaultdict(int)

    def add_course(self, course: str) -> None:
        """ Method to add a course to the students course dictionary """
        self._courses[course] += 1

    def prettytable_rows(self) -> Iterator[Tuple[str, str, str, str, int]]:
        """ Method to return the data for a prettytable as a tuple """
        for course, num_students in self._courses.items():
            yield self._cwid, self._name, self._department, course, num_students
