import unittest
from server import process_os_command, process_math_command

class TestServerFunctions(unittest.TestCase):

    def test_process_os_command(self):
        # Test the OS command processing
        result = process_os_command("echo", ["Hello, World!"])
        self.assertEqual(result["status"], "success")
        self.assertIn("Hello, World!", result["result"])

    def test_process_math_command(self):
        # Test the math command processing
        result = process_math_command("(2 + 3) * 4")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["result"], 20)

    def test_process_invalid_command(self):
        # Test handling an invalid math expression
        result = process_math_command("invalid_expression")
        self.assertEqual(result["status"], "error")
        self.assertIn("Invalid variable name in expression", result["message"])

if __name__ == '__main__':
    unittest.main()
