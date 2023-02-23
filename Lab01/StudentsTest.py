import unittest
import Students

class Test(unittest.TestCase):
    students = Students.Students()

    user_name = ['John', 'Mary','Thomas','Jane']
    user_id = []
 
    def test_0_set_name(self):
        print("Start set_name test\n")
        for name in self.user_name:
            id = self.students.set_name(name)
            self.assertNotIn(id, self.user_id)
            self.user_id.append(id)
            print(id , name)
        print("\nFinish set_name test\n")

        
    def test_1_get_name(self):
        print("\n\nStart get_name test\n")
        print("\nuser_id length = ", len(self.user_id))
        print("user_name length = ", len(self.user_id), "\n")
        for i in range(0, len(self.user_id)):
            name = self.students.get_name(self.user_id[i])
            self.assertEqual(name, self.user_name[i])
            print("id", self.user_id[i], ":", self.user_name[i])
        name = self.students.get_name(len(self.user_id))
        self.assertEqual(name, "There is no such user")
        print("id", len(self.user_id), ":", self.students.get_name(len(self.user_id)))
        print("\nFinish get_name test\n")
