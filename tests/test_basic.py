import unittest
from cron_parser.parser import TimePeriod, validate_command


class TestStringMethods(unittest.TestCase):

    def test_valid_cron_commands(self):
        # Command without parameters
        res = validate_command("1,2-3,*/5    0    1,15   *   1,4-6 /path/to/script.sh")
        self.assertIs(TimePeriod, type(res[0]))

        res = validate_command("   1,2-3,*/5    0    1,15   *   1,4-6 /path/to/script.sh")
        self.assertIs(TimePeriod, type(res[0]))

        # Command with parameters
        res = validate_command("   1,2-3,*/5    0    1,15   *   1,4-6 /bin/bash /path/to/script.sh       ")
        self.assertIs(TimePeriod, type(res[0]))

        res = validate_command("   1,2-3,*/5    0    1,15   *   1,4-6 /bin/bash /path/to/script.sh")
        self.assertIs(TimePeriod, type(res[0]))

        res = validate_command("1,2-3,*/5    0    1,15   *   1,4-6 \"/bin/bash /path/to/script.sh\"       ")
        self.assertIs(TimePeriod, type(res[0]))

    def test_invalid_cron_commands(self):
        self.assertRaises(ValueError, validate_command, "")
        self.assertRaises(ValueError, validate_command, "*")
        self.assertRaises(ValueError, validate_command, "* *")
        self.assertRaises(ValueError, validate_command, "* * *")
        self.assertRaises(ValueError, validate_command, "* * * *")
        self.assertRaises(ValueError, validate_command, "* * * * *")
        self.assertRaises(ValueError, validate_command, "*  * *  *   *  ")
        self.assertRaises(ValueError, validate_command, "  *  * *  *   *  ")

    def test_range_validation(self):
        # Single value that's out of bounds
        self.assertRaises(ValueError, validate_command, "71 17 26 11 5 /bin/bash /path/to/script.sh")
        # Range that's out of bounds
        self.assertRaises(ValueError, validate_command, "45-61 17 26 11 5 /bin/bash /path/to/script.sh")
        # Multiple values, one being out of bounds
        self.assertRaises(ValueError, validate_command, "45 17,25 26 11 5 /bin/bash /path/to/script.sh")
        # Division by zero
        self.assertRaises(ValueError, validate_command, "45/0 17 26 11 5 /bin/bash /path/to/script.sh")

    def test_interval_contents(self):
        minute, hour, day, month, weekday, command = validate_command("1,2-3,*/5 0 1,15 * 1,4-6 /bin/bash /path/to/script.sh")
        self.assertEqual(minute.get_contents(), [0, 1, 2, 3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
        self.assertEqual(hour.get_contents(), [0])
        self.assertEqual(day.get_contents(), [1, 15])
        self.assertEqual(month.get_contents(), [m for m in range(1, 13)])
        self.assertEqual(weekday.get_contents(), [1, 4, 5, 6])
        self.assertEqual(command.get_contents(), "/bin/bash /path/to/script.sh")


if __name__ == '__main__':
    unittest.main()
