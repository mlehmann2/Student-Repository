"""
@author Margie Lehmann
This program collects university data repository and stores it as classes, and students, and instructors.
"""

from prettytable import PrettyTable
from typing import Tuple, Iterator, Dict, IO
import os
import Student
import Instructor


class University:
    """ Class to take a universities data repository and organize it """

    def __init__(self, univ_directory: str) -> None:
        """ Method to initialize the University with the data repo """
        # CWID to Student
        self._students_dict: Dict[str, Student.Student] = dict()
        # CWID to Instructor
        self._instructors_dict: Dict[str, Instructor.Instructor] = dict()

        # Verify directory exists
        self._univ_directory = univ_directory
        if os.path.isdir(self._univ_directory):
            # Populate the students, instructors, and grades
            self._populate_students()
            self._populate_instructors()
            self._populate_grades()

        else:
            raise FileNotFoundError(
                f"{self._univ_directory} is not a valid university.")

    def _populate_students(self) -> None:
        """ Method to populate the Student data dictionary """
        # Populate the students
        path: str = os.path.join(self._univ_directory, 'students.txt')
        reader = self._file_reader(path, 3, sep='\t', header=False)
        for cwid, name, major in reader:
            self._students_dict[cwid] = Student.Student(cwid, name, major)

    def _populate_instructors(self) -> None:
        """ Method to populate the Instructor data dictionary """
        # Populate the students
        path: str = os.path.join(self._univ_directory, 'instructors.txt')
        reader = self._file_reader(path, 3, sep='\t', header=False)
        for cwid, name, department in reader:
            self._instructors_dict[cwid] = Instructor.Instructor(
                cwid, name, department)

    def _populate_grades(self) -> None:
        """ Method to populate grade and class data for students and instructors """
        path: str = os.path.join(self._univ_directory, 'grades.txt')
        reader = self._file_reader(path, 4, sep='\t', header=False)
        for grade_info in reader:
            if grade_info[3] in self._instructors_dict.keys():
                if grade_info[0] in self._students_dict.keys():
                    self._students_dict[grade_info[0]].add_course(
                        grade_info[1], grade_info[2])
                    self._instructors_dict[grade_info[3]].add_course(
                        grade_info[1])
                else:
                    print(
                        f'{grade_info[0]} is not a valid student CWID. - Skipping grade.')
            else:
                print(
                    f'{grade_info[3]} is not a valid instructor CWID. - Skipping grade.')

    def _file_reader(self, path: str, fields: int, sep: str = ',',
                     header: bool = False) -> Iterator[Tuple[str]]:
        """ Generator to read one line from a file at a time and return its output as a tuple seperated by the specified seperator """
        try:
            file: IO = open(path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(
                f"{path} file not found for {self._univ_directory}")
        else:
            with file:
                for n, line in enumerate(file, 1):
                    ret: Tuple[str] = tuple(line.rstrip('\n').split(sep))
                    if len(ret) != fields:
                        print(
                            f'{path} line {n} has {len(ret)} fields but is expected to have {fields} fields.  - Skipping this line.')
                    elif n == 1 and header:
                        continue
                    else:
                        yield ret

    def pretty_print_students(self) -> None:
        """ Method to print the student dictionary as a pretty table """
        print(f"Summary for {self._univ_directory} students.")

        pt: PrettyTable = PrettyTable(
            field_names=Student.Student.prettytable_header)
        for student in self._students_dict.values():
            pt.add_row(student.prettytable_row())
        print(pt)

    def pretty_print_instructors(self) -> None:
        """ Method to print the instructor dictionary as a pretty table """
        print(f"Summary for {self._univ_directory} instructors.")

        pt: PrettyTable = PrettyTable(
            field_names=Instructor.Instructor.prettytable_header)
        for instructor in self._instructors_dict.values():
            for row in instructor.prettytable_rows():
                pt.add_row(row)
        print(pt)
