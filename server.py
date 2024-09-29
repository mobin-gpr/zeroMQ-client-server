import zmq
import os
import logging
from colorama import Fore, init
from threading import Thread

# Configure logging to log all actions to 'server.log'
logging.basicConfig(
    filename="server.log", level=logging.INFO, format="%(asctime)s - %(message)s"
)

# Initialize Colorama for colorful output in the terminal
init(autoreset=True)


def process_os_command(command_name, parameters):
    """
    Executes an OS command with the given parameters.

    Args:
        command_name (str): The name of the OS command to execute (e.g., 'ping').
        parameters (list): A list of parameters to pass to the command.

    Returns:
        dict: A dictionary containing the execution status ('success' or 'error')
              and the result or error message.
    """
    try:
        # Use with statement to ensure the file is closed properly
        with os.popen(f"{command_name} {' '.join(parameters)}") as pipe:
            result = pipe.read()
        logging.info(f"Executed OS Command: {command_name} {parameters}")
        return {"status": "success", "result": result}
    except Exception as e:
        logging.error(f"Error executing OS command: {str(e)}")
        return {"status": "error", "message": str(e)}


def process_math_command(expression):
    """
    Evaluates a mathematical expression.

    Args:
        expression (str): The arithmetic expression to evaluate (e.g., "(2 + 3) * 4").

    Returns:
        dict: A dictionary containing the evaluation status ('success' or 'error')
              and the result or error message.
    """
    try:
        # Evaluate the mathematical expression
        result = eval(expression)
        logging.info(f"Computed Math Expression: {expression} = {result}")
        return {"status": "success", "result": result}
    except SyntaxError:
        # Handle syntax errors specifically
        logging.error(f"Syntax error in math computation: {expression}")
        return {"status": "error", "message": "Invalid expression syntax"}
    except NameError:
        # Handle name errors specifically
        logging.error(f"Name error in math computation: {expression}")
        return {"status": "error", "message": "Invalid variable name in expression"}
    except Exception as e:
        # Catch all other exceptions
        logging.error(f"Error in math computation: {str(e)}")
        return {"status": "error", "message": str(e)}


def worker_routine(context, worker_id):
    """
    Worker routine to process client requests in a separate thread.

    Args:
        context (zmq.Context): The ZeroMQ context used to create and manage sockets.
        worker_id (int): The unique ID of the worker (used for logging and debugging).

    This function runs indefinitely, receiving requests from the DEALER socket,
    processing them based on the command type, and sending back the result.
    """
    # Create a REP socket for this worker and connect it to the internal DEALER socket
    socket = context.socket(zmq.REP)
    socket.connect("inproc://workers")  # Connect to the internal in-process socket

    # Log the start of the worker
    print(Fore.CYAN + f"Worker {worker_id} started and ready to process requests...")
    logging.info(f"Worker {worker_id} started and ready to process requests...")

    while True:
        # Receive a JSON message from the client via the DEALER-REP architecture
        message = socket.recv_json()
        logging.info(f"Worker {worker_id} received message: {message}")

        # Determine the type of command and process it
        if message["command_type"] == "os":
            response = process_os_command(
                message["command_name"], message["parameters"]
            )
        elif message["command_type"] == "compute":
            response = process_math_command(message["expression"])
        else:
            # If the command type is invalid, return an error response
            response = {"status": "error", "message": "Invalid command type"}
            logging.error(f"Worker {worker_id}: Invalid command type received")

        # Log the response being sent back to the client
        logging.info(f"Worker {worker_id} sending response: {response}")

        # Send the response back to the client
        socket.send_json(response)


def main():
    """
    Main server function that listens for incoming client requests,
    distributes them to worker threads, and handles them concurrently.

    This function sets up the ROUTER socket for incoming client connections and
    a DEALER socket for distributing the requests to worker threads. The zmq.proxy
    function is used to handle the routing of messages between clients and workers.
    """
    # Create a ZeroMQ context
    context = zmq.Context()

    # Create a ROUTER socket to accept client connections on port 5555
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://*:5555")

    # Create a DEALER socket to distribute work to worker threads
    backend = context.socket(zmq.DEALER)
    backend.bind("inproc://workers")

    # Log that the server has started
    print(Fore.GREEN + "Server is running and listening on port 5555...")
    logging.info("Server started and listening on port 5555")

    # Start worker threads to handle requests
    for i in range(5):
        # Create and start a worker thread with a unique worker ID
        worker = Thread(target=worker_routine, args=(context, i))
        worker.start()

    # Use a zmq.proxy to route client requests to worker threads
    zmq.proxy(frontend, backend)


if __name__ == "__main__":
    main()
