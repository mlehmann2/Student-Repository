"""
@author Margie Lehmann
This file contains the Student class for out Univeristy data tracking program.
"""

from typing import Tuple, Dict, List


class Student:
    """ Class to student data """
    prettytable_header: List[str] = ['CWID', 'Name', 'Completed Courses']

    y = 2

    def __init__(self, cwid: str, name: str, major: str) -> None:
        """ Method to initialize a Student """
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        # Course to grade
        self._courses: Dict[str, str] = dict()

    def add_course(self, course: str, grade: str) -> None:
        """ Method to add a course to the students course dictionary """
        self._courses[course] = grade

    def prettytable_row(self) -> Tuple[str, str, List[str]]:
        """ Method to return the data for a prettytable as a tuple """
        return self._cwid, self._name, sorted(self._courses.keys())
