import zmq
from colorama import Fore, init
import platform

# Initialize Colorama for colorful output in the terminal
init(autoreset=True)


def send_command(command):
    """
    Sends a JSON command to the server and waits for the response.

    Args:
        command (dict): The command to send to the server in JSON format.

    Returns:
        dict: The server's response in JSON format, containing either the result or an error message.
    """
    # Use with statement to ensure that the context and socket are properly closed
    with zmq.Context() as context:
        with context.socket(zmq.REQ) as socket:
            # Connect the socket to the server's address (localhost:5555)
            socket.connect("tcp://localhost:5555")

            # Print the command being sent in yellow
            print(Fore.YELLOW + f"Sending command: {command}")

            # Send the command as JSON to the server
            socket.send_json(command)

            # Notify the user that we are waiting for the server's response
            print(Fore.YELLOW + "Waiting for response from server...")

            # Receive the response from the server
            response = socket.recv_json()

            # Print the received response in green
            print(Fore.GREEN + f"Received response: {response}")

            # Return the server's response
            return response


if __name__ == "__main__":

    # Detect the current operating system
    current_os = platform.system()

    # Example OS command: "ping 127.0.0.1"
    # Set the ping command based on the OS
    if current_os == "Windows":
        os_command = {
            "command_type": "os",
            "command_name": "ping",
            "parameters": [
                "127.0.0.1",
                "-n",
                "5",
            ],  # '-n' for Windows to limit ping count to 5
        }
    else:
        os_command = {
            "command_type": "os",
            "command_name": "ping",
            "parameters": [
                "127.0.0.1",
                "-c",
                "5",
            ],  # '-c' for Linux/macOS to limit ping count to 5
        }

    # Example math command: "(6 + 4) * 8"
    math_command = {
        "command_type": "compute",
        "expression": "(6 + 4) * 8",  # Simple arithmetic expression
    }

    # Sending the OS command (ping) and printing a visual separator
    print(Fore.CYAN + "Sending OS command:")
    send_command(os_command)

    # Print a separator line for better readability
    print("-" * 55)

    # Sending the math command and printing a visual separator
    print(Fore.CYAN + "Sending Math command:")
    send_command(math_command)
