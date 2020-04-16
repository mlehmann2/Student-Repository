"""
@author Margie Lehmann
This program collects university data repository and stores it as classes, and students, and instructors.
"""

from collections import defaultdict
from prettytable import PrettyTable
from typing import Tuple, Iterator, Dict, IO, List
import os
import sqlite3
import Student
import Instructor
import Major


class University:
    """ Class to take a universities data repository and organize it """

    def __init__(self, univ_directory: str) -> None:
        """ Method to initialize the University with the data repo """
        # CWID to Student
        self._students_dict: Dict[str, Student.Student] = dict()
        # CWID to Instructor
        self._instructors_dict: Dict[str, Instructor.Instructor] = dict()
        # Major to Major data
        self._major_dict: Dict[str, Major.Major] = dict()

        # Verify directory exists
        self._univ_directory = univ_directory
        if os.path.isdir(self._univ_directory):
            # Populate the students, instructors, and grades
            self._populate_majors()
            self._populate_students()
            self._populate_instructors()
            self._populate_grades()

        else:
            raise FileNotFoundError(
                f"{self._univ_directory} is not a valid university.")

    def _populate_majors(self) -> None:
        """ Method to populate major data for a major """
        path: str = os.path.join(self._univ_directory, 'majors.txt')
        reader = self._file_reader(path, 3, sep='\t', header=True)
        for name, type, course in reader:
            # Verify instructor and student exist
            if name not in self._major_dict.keys():
                self._major_dict[name] = Major.Major(name)
            self._major_dict[name].add_course(type, course)

    def _populate_students(self) -> None:
        """ Method to populate the Student data dictionary """
        # Populate the students
        path: str = os.path.join(self._univ_directory, 'students.txt')
        reader = self._file_reader(path, 3, sep='\t', header=True)
        for cwid, name, major in reader:
            if major in self._major_dict.keys():
                self._students_dict[cwid] = Student.Student(
                    cwid, name, self._major_dict[major])
            else:
                print(
                    f'{major} is not a valid major. - Skipping Student {cwid}.')

    def _populate_instructors(self) -> None:
        """ Method to populate the Instructor data dictionary """
        # Populate the students
        path: str = os.path.join(self._univ_directory, 'instructors.txt')
        reader = self._file_reader(path, 3, sep='\t', header=True)
        for cwid, name, department in reader:
            self._instructors_dict[cwid] = Instructor.Instructor(
                cwid, name, department)

    def _populate_grades(self) -> None:
        """ Method to populate grade and class data for students and instructors """
        path: str = os.path.join(self._univ_directory, 'grades.txt')
        reader = self._file_reader(path, 4, sep='\t', header=True)
        for s_cwid, course, grade, i_cwid in reader:
            # Verify instructor and student exist
            if i_cwid in self._instructors_dict.keys():
                if s_cwid in self._students_dict.keys():
                    self._students_dict[s_cwid].add_course(course, grade)
                    self._instructors_dict[i_cwid].add_course(course)
                else:
                    print(
                        f'{s_cwid} is not a valid student CWID. - Skipping grade.')
            else:
                print(
                    f'{i_cwid} is not a valid instructor CWID. - Skipping grade.')

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

    def pretty_print_majors(self) -> None:
        """ Method to print the student dictionary as a pretty table """
        print(f"Summary for {self._univ_directory} majors.")

        pt: PrettyTable = PrettyTable(
            field_names=Major.Major.prettytable_header)
        for major in self._major_dict.values():
            pt.add_row(major.prettytable_row())
        print(pt)

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

    def student_grades_table_db(self, db_path) -> None:
        """ Method to pretty print the student grades table """
        print(f"Summary for {self._univ_directory} student's grades.")

        pt: PrettyTable = PrettyTable(
            field_names=['Name', 'CWID', 'Course', 'Grade', 'Instructor'])

        for row in self._database_query(db_path):
            pt.add_row(row)

        print(pt)

    def _database_query(self,
                        db_path) -> Iterator[Tuple[str, str, str, str, str]]:
        """ Generator to query the university DB and return a student grades row one at a time """
        try:
            db: sqlite3.Connection = sqlite3.connect(db_path)
        except sqlite3.OperationalError:
            print(f"The path to the database is not a proper DB: {db_path}")
        else:
            query: str = """ SELECT s.Name, s.CWID, g.Course, g.Grade, i.Name
            FROM students s JOIN grades g ON s.CWID = g.StudentCWID
            JOIN instructors i ON g.InstructorCWID = i.CWID
            ORDER BY s.Name """

            for row in db.execute(query):
                yield row
