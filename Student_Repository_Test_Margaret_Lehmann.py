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

    def test_students_dictionary(self) -> None:
        """ Test the university classes student dict """
        expected = {'10103': ('10103', 'Baldwin, C', ['CS 501', 'SSW 564'])}

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


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
