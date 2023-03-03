import unittest
import app
from unittest.mock import Mock


class ApplicationTest(unittest.TestCase):
    myapp = app
    name_list = ["Willian", "Oilver", "Henry", "Liam"]
    selected_list = ["Willian", "Oilver", "Henry"]

    def setUp(self):

        print("Start setUp\n")

        # stub
        mock_get_names = Mock()
        mock_get_names.return_value = (self.name_list, self.selected_list)
        app.Application.get_names = mock_get_names
        self.myapp = app.Application()

        print("Finish setUp\n")

    def test_app(self):

        print("Start test_app\n")

        # mock
        mock_get_random_person = Mock()
        mock_get_random_person.side_effect = self.name_list
        app.Application.get_random_person = mock_get_random_person
        # print(self.myapp.get_random_person())
        # print(self.myapp.get_random_person())
        # print(self.myapp.get_random_person())
        # print(self.myapp.get_random_person())
        selected = self.myapp.select_next_person()
        self.assertEqual(selected, "Liam")
        print(selected, "selected")

        # spy
        def fake_write(name):
            context = 'Congrats, ' + name + '!'
            return context

        def fake_send(name, context):
            print(context)

        mock_write = Mock()
        mock_write.side_effect = fake_write
        app.MailSystem.write = mock_write

        mock_send = Mock()
        mock_send.side_effect = fake_send
        app.MailSystem.send = mock_send

        self.myapp.notify_selected()
        self.assertEqual(mock_write.call_count, len(self.name_list))
        self.assertEqual(mock_send.call_count, len(self.name_list))

        print("Finish test_app\n")

        # print(mock_get_random_person.call_args_list)
        print(mock_write.call_args_list)
        print(mock_send.call_args_list)


if __name__ == "__main__":
    unittest.main()
