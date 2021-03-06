"""
@author Margie Lehmann
This file contains the Major class for out Univeristy data tracking program.
"""

from typing import Tuple, Dict, List, Set


class Major:
    """ Class to hold Major data """
    prettytable_header: List[str] = ['Major', 'Required Courses', 'Electives']

    passing_grades: List[str] = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']

    def __init__(self, name: str) -> None:
        """ Method to initialize a Major """
        self._name: str = name
        self._required: Set[str] = set()
        self._electives: Set[str] = set()

    def add_course(self, type: str, course: str) -> None:
        """ Method to add a course to the students course dictionary """
        if type == 'R':
            self._required.add(course)
        elif type == 'E':
            self._electives.add(course)
        else:
            print(
                f'{type} is an invalid type for course {course}. - Not adding course to major {self._name}')

    def get_course_summary(self, course_dict: Dict[str, str]) -> Tuple[Set[str], Set[str], Set[str]]:
        """ Method to return remaining courses given a set of courses """
        courses = set(
            [course for course, grade in course_dict.items() if grade in self.passing_grades])

        if courses.intersection(self._electives) == set():
            return courses, self._required.difference(courses), self._electives
        else:
            return courses, self._required.difference(courses), {}

    def prettytable_row(self) -> Tuple[str, str, List[str]]:
        """ Method to return the data for a prettytable as a tuple """
        return self._name, sorted(self._required), sorted(self._electives)
