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