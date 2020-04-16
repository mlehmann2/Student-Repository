"""
@author Margie Lehmann
This program uses unit tests the unversity information data classes.
"""

from typing import Dict
import unittest
import Student_Repository_Margaret_Lehmann as University
import Student
import Instructor


class UniversityTest(unittest.TestCase):
    """ Class to test the university data classes """

    def test_majors_dictionary(self) -> None:
        """ Test the university classes student dict """
        expected = {'SFEN': ('SFEN', ['SSW 540', 'SSW 564'], ['CS 501'])}

        univ: University.University = University.University('Syracuse')
        calculated = {name: major.prettytable_row()
                      for name, major in univ._major_dict.items()}

        self.assertEqual(expected, calculated)

    def test_students_dictionary(self) -> None:
        """ Test the university classes student dict """
        expected = {'10103': ('10103', 'Baldwin, C', [
                              'CS 501', 'SSW 564'], ['SSW 540'], [], 3.38)}

        univ: University.University = University.University('Syracuse')
        calculated = {cwid: student.prettytable_row()
                      for cwid, student in univ._students_dict.items()}

        self.assertEqual(expected, calculated)

    def test_instructors_dictionary(self) -> None:
        """ Test the university classes instructors dict """
        expected = {('98764', 'Feynman, R', 'SFEN', 'SSW 564', 1),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1)}

        univ: University.University = University.University('Syracuse')

        calculated = {info for instructor in univ._instructors_dict.values()
                      for info in instructor.prettytable_rows()}

        self.assertEqual(expected, calculated)

    def test_invalid_directory(self) -> None:
        """ Test the university classes returns an invalid directory message """
        with self.assertRaises(FileNotFoundError):
            univ: University.University = University.University('Binghamton')

    def test_missing_file(self) -> None:
        """ Test the university classes returns an missing file message """
        with self.assertRaises(FileNotFoundError):
            univ: University.University = University.University('Cornell')

    def test_student_grades_table_db(self) -> None:
        """ Test the method that queries the database """
        expected = [('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'),
                    ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'),
                    ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'),
                    ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'),
                    ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S'),
                    ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'),
                    ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'),
                    ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'),
                    ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J')]

        univ: University.University = University.University('Stevens')
        iter = univ._database_query(
            "/Users/Margie/Desktop/SSW-810 Spring 2020/university_database.db")

        self.assertEqual(expected, list(iter))


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
