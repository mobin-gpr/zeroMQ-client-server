import zmq
from colorama import Fore, init

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
    # Create a ZeroMQ context for communication
    context = zmq.Context()

    # Create a socket of type REQ (request) to send a command and expect a response
    socket = context.socket(zmq.REQ)

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
    # Example OS command: "ping 127.0.0.1"
    os_command = {
        "command_type": "os",
        "command_name": "ping",
        "parameters": ["127.0.0.1"],  # Parameters for the 'ping' command
    }

    # Example math command: "(2 + 3) * 4"
    math_command = {
        "command_type": "compute",
        "expression": "(6 + 4) * 8",  # Simple arithmetic expression
    }

    # Sending the OS command (ping) and printing a visual separator
    print(Fore.CYAN + "Sending OS command:")
    send_command(os_command)

    # Print a separator line for better readability
    print("-" * 60)

    # Sending the math command and printing a visual separator
    print(Fore.CYAN + "Sending Math command:")
    send_command(math_command)
