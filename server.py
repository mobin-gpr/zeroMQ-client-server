import zmq
import os
import json
import logging
from threading import Thread

# Configure logging to log all actions to 'server.log'
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def process_os_command(command_name, parameters):
    """
    Executes an OS command with the given parameters.

    Args:
        command_name (str): The OS command to execute (e.g., 'ping').
        parameters (list): A list of parameters to pass to the command.

    Returns:
        dict: A dictionary containing the execution status ('success' or 'error') and the result or error message.
    """
    try:
        # Execute the OS command and capture the output
        result = os.popen(f"{command_name} {' '.join(parameters)}").read()
        logging.info(f"Executed OS Command: {command_name} {parameters}")
        return {"status": "success", "result": result}
    except Exception as e:
        # Log any error that occurs during command execution
        logging.error(f"Error executing OS command: {str(e)}")
        return {"status": "error", "message": str(e)}


def process_math_command(expression):
    """
    Evaluates a mathematical expression.

    Args:
        expression (str): The arithmetic expression to evaluate (e.g., "(2 + 3) * 4").

    Returns:
        dict: A dictionary containing the evaluation status ('success' or 'error') and the result or error message.
    """
    try:
        # Evaluate the arithmetic expression
        result = eval(expression)
        logging.info(f"Computed Math Expression: {expression} = {result}")
        return {"status": "success", "result": result}
    except Exception as e:
        # Log any error that occurs during expression evaluation
        logging.error(f"Error in math computation: {str(e)}")
        return {"status": "error", "message": str(e)}


def handle_request(socket):
    """
    Handles incoming client requests, processes them, and sends back the result.

    Args:
        socket (zmq.Socket): The ZeroMQ REP socket used for communication with the client.
    """
    while True:
        try:
            # Wait for a message from the client
            logging.info("Waiting to receive a message from the client...")
            message = socket.recv_json()
            logging.info(f"Received message: {message}")

            # Determine the type of command and process it accordingly
            if message["command_type"] == "os":
                response = process_os_command(message["command_name"], message["parameters"])
            elif message["command_type"] == "compute":
                response = process_math_command(message["expression"])
            else:
                # If the command type is invalid, send an error response
                response = {"status": "error", "message": "Invalid command type"}
                logging.error("Invalid command type received")

            # Send the response back to the client
            logging.info(f"Sending response: {response}")
            socket.send_json(response)
        except json.JSONDecodeError:
            # If there is a JSON decoding error, log it and send an error response
            socket.send_json({"status": "error", "message": "Invalid JSON format"})
            logging.error("Invalid JSON format received")


def main():
    """
    Initializes the server, binds it to a port, and handles client requests concurrently using threads.
    """
    # Create a ZeroMQ context and a REP socket
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    # Bind the socket to port 5555 to listen for incoming client requests
    socket.bind("tcp://*:5555")

    print("Server is running and listening on port 5555...")
    logging.info("Server started and listening on port 5555")

    # Create multiple threads to handle concurrency, all sharing the same socket
    for _ in range(5):
        worker = Thread(target=handle_request, args=(socket,))
        worker.start()


if __name__ == "__main__":
    main()
