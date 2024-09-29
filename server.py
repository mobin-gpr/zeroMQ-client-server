import zmq
import os
import json
import logging
from threading import Thread

# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def process_os_command(command_name, parameters):
    """
    Executes the given OS command with the specified parameters.

    Args:
        command_name (str): The name of the OS command to execute.
        parameters (list): List of parameters for the command.

    Returns:
        dict: A dictionary containing the status (success/error) and the result or error message.
    """
    try:
        result = os.popen(f"{command_name} {' '.join(parameters)}").read()
        logging.info(f"Executed OS Command: {command_name} {parameters}")
        return {"status": "success", "result": result}
    except Exception as e:
        logging.error(f"Error executing OS command: {str(e)}")
        return {"status": "error", "message": str(e)}


def process_math_command(expression):
    """
    Evaluates a simple arithmetic expression.

    Args:
        expression (str): The arithmetic expression to evaluate.

    Returns:
        dict: A dictionary containing the status (success/error) and the result or error message.
    """
    try:
        result = eval(expression)
        logging.info(f"Computed Math Expression: {expression} = {result}")
        return {"status": "success", "result": result}
    except Exception as e:
        logging.error(f"Error in math computation: {str(e)}")
        return {"status": "error", "message": str(e)}


def handle_request(socket):
    """
    Handles incoming requests from clients.

    Args:
        socket (zmq.Socket): The ZeroMQ socket to receive and send messages.
    """
    while True:
        try:
            message = socket.recv_json()
            if message["command_type"] == "os":
                response = process_os_command(message["command_name"], message["parameters"])
            elif message["command_type"] == "compute":
                response = process_math_command(message["expression"])
            else:
                response = {"status": "error", "message": "Invalid command type"}
                logging.error("Invalid command type received")

            socket.send_json(response)
        except json.JSONDecodeError:
            socket.send_json({"status": "error", "message": "Invalid JSON format"})
            logging.error("Invalid JSON format received")