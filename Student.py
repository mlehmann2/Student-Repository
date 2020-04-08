"""
@author Margie Lehmann
This file contains the Student class for out Univeristy data tracking program.
"""

from typing import Tuple, Dict, List


class Student:
    """ Class to student data """
    prettytable_header: List[str] = ['CWID', 'Name', 'Completed Courses']

    grade_to_value: Dict[str, float] = {
        'A': 4.0, 'A-': 3.75, 'B+': 3.25, 'B': 3.0, 'B-': 2.75, 'C+': 2.25, 'C': 2.0, 'C-': 0.0, 'D+': 0.0, 'D': 0.0, 'D-': 0.0, 'F': 0.0}

    passing_grades: List[str] = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']

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

    def calculate_gpa(self) -> float:
        """ Method to calculate a return the students GPA """
        gpa: float = 0.0
        for grade in self._courses.values():
            gpa += self.grade_to_value[grade]
        return gpa / len(self._courses)

    def prettytable_row(self) -> Tuple[str, str, List[str]]:
        """ Method to return the data for a prettytable as a tuple """
        return self._cwid, self._name, sorted(self._courses.keys())
