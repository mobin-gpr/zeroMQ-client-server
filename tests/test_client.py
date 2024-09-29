import unittest
from client import send_command


class TestClient(unittest.TestCase):

    def test_send_os_command(self):
        # Test sending an OS command and receiving a response
        os_command = {
            "command_type": "os",
            "command_name": "echo",
            "parameters": ["Hello, World!"],
        }
        response = send_command(os_command)
        self.assertEqual(response["status"], "success")
        self.assertIn("Hello, World!", response["result"])

    def test_send_math_command(self):
        # Test sending a math command and receiving a response
        math_command = {"command_type": "compute", "expression": "(10 + 5) * 4"}
        response = send_command(math_command)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["result"], 60)


if __name__ == "__main__":
    unittest.main()
