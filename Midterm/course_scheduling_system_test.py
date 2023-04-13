import unittest
import course_scheduling_system
from unittest.mock import Mock


class CSSTest(unittest.TestCase):
    course_ST = ("SoftwareTesting", "Thursday", 5, 6)
    course_OSDI = ("OSDI", "Wednesday", 1, 2)    
    course_ICLAB = ("ICLAB", "Wednesday", 3, 4)

    course_fake = ("FakeCourse", "Thursday", 5, 6)

    def setUp(self):
        self.myCSS = course_scheduling_system.CSS()

    def test_q1_1(self):
        mock_check_course_exist = Mock()
        mock_check_course_exist.return_value = True
        course_scheduling_system.CSS.check_course_exist = mock_check_course_exist
        with self.subTest():
            self.assertEqual(self.myCSS.add_course(self.course_ST), True)
        with self.subTest():
            self.assertIn(self.course_ST, self.myCSS.get_course_list())

    def test_q1_2(self):
        mock_check_course_exist = Mock()
        mock_check_course_exist.return_value = True
        course_scheduling_system.CSS.check_course_exist = mock_check_course_exist
        with self.subTest():
            self.assertEqual(self.myCSS.add_course(self.course_ST), True)
            self.assertEqual(self.myCSS.add_course(self.course_fake), False)
        with self.subTest():
            self.assertNotIn(self.course_fake, self.myCSS.get_course_list())

    def test_q1_3(self):
        mock_check_course_exist = Mock()
        mock_check_course_exist.return_value = False
        course_scheduling_system.CSS.check_course_exist = mock_check_course_exist
        # self.myCSS.add_course(self.course_ST)
        with self.subTest():
            self.assertEqual(self.myCSS.add_course(self.course_ST), False)
        # print(self.myCSS.add_course(self.course_ST))

    def test_q1_4(self):
        with self.subTest():
            with self.assertRaises(TypeError):
                self.myCSS.add_course("INVALID COURSE")



    def test_q1_5(self):
        mock_check_course_exist = Mock()
        mock_check_course_exist.return_value = True
        course_scheduling_system.CSS.check_course_exist = mock_check_course_exist

        with self.subTest():
            self.assertEqual(self.myCSS.add_course(self.course_ST), True)
            self.assertEqual(self.myCSS.add_course(self.course_OSDI), True)
            self.assertEqual(self.myCSS.add_course(self.course_ICLAB), True)
            self.assertEqual(self.myCSS.remove_course(self.course_OSDI), True)
            self.assertNotIn(self.course_OSDI, self.myCSS.get_course_list())
            self.assertEqual(course_scheduling_system.CSS.check_course_exist.call_count, 4)
        print(self.myCSS)

    def test_q1_6(self):
        course_fake_1 = (88888, "Thursday", 5, 6)
        course_fake_2 = ("fake", "Sunday", 5, 6)
        course_fake_3 = ("fake", "Thursday", '5', 6)
        
        with self.subTest():
            with self.assertRaises(TypeError):
                self.myCSS.add_course(course_fake_1)
            with self.assertRaises(TypeError):
                self.myCSS.add_course(course_fake_2)
            with self.assertRaises(TypeError):
                self.myCSS.add_course(course_fake_3)

        mock_check_course_exist = Mock()
        mock_check_course_exist.return_value = False
        course_scheduling_system.CSS.check_course_exist = mock_check_course_exist
        with self.subTest():
            self.assertEqual(self.myCSS.remove_course(self.course_ST), False)

        mock_check_course_exist = Mock()
        mock_check_course_exist.return_value = True
        course_scheduling_system.CSS.check_course_exist = mock_check_course_exist
        self.myCSS.remove_course(self.course_ST)
        with self.subTest():
            self.assertEqual(self.myCSS.remove_course(self.course_ST), False)

if __name__ == "__main__":
    unittest.main()
