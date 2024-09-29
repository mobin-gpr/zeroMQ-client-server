# Client-Server Application using ZeroMQ

This project implements a simple client-server architecture where the server can process two types of commands:
1. OS Commands (e.g., `ping`)
2. Math Commands (e.g., simple arithmetic expressions)

The communication between the client and server is handled using **ZeroMQ**.

## Features:
- **Command Logging**: All commands and results are logged to `server.log`.
- **Concurrency**: Server can handle multiple requests concurrently using threads.
- **Unit Tests**: Both the client and server have unit tests to verify functionality.

## Requirements

- Python 3.x
- ZeroMQ library for Python (`pyzmq`)
- Colorama

You can install the required library using:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Running the Server

To start the server, simply run the following command in the terminal:

```bash
python server.py
```
The server will start and begin listening on port 5555 for incoming client requests. The server is capable of handling multiple requests concurrently using threading.

### 2. Running the Client

You can send commands to the server using the client. To run the client and send example commands (OS command and a math command):

```bash
python client.py
```

The client sends an OS command (ping 127.0.0.1) and a math command ((6 + 4) * 8) to the server. The server processes the commands and sends back the results, which will be displayed in the terminal.



### 3. Custom Commands

```python
# Example OS command:
os_command = {
    "command_type": "os",
    "command_name": "ping",
    "parameters": ["127.0.0.1"]
}

# Example math command:
math_command = {
    "command_type": "compute",
    "expression": "(6 + 4) * 8"
}
```

### 4. Running the Tests

The project contains unit tests for both the client and the server. You can run the tests using the following command:


```bash
python -m unittest discover -s tests
```

This command will automatically discover and execute all test files in the tests directory.

### 5. Logging

All the commands sent to the server and their results are logged into the  `server.log` file. You can view the log file to see a history of all commands and their respective results.

## ⚠️ Security Warning

This project is intended for testing and educational purposes only and is not suitable for use in professional or production environments. Executing operating system commands and evaluating mathematical expressions from client inputs can pose serious security risks. Before using this project in sensitive environments, please consider the following:

### 1. Preventing the Execution of Malicious Code:
Input Validation: Inputs from the client should be thoroughly examined and validated before execution to prevent the execution of malicious commands.
Restricting Allowed Commands: Only allow specific, safe operating system commands to be executed, limiting access to dangerous commands.
### 2. Using Safer Methods for Evaluating Mathematical Expressions:
Replacing eval: Using the eval function can lead to the execution of malicious code. Instead, consider using safer libraries such as ast.literal_eval or specialized mathematical libraries.
### 3. Authentication and Authorization:
Implementing Authentication: Ensure that only authorized users can access the server before processing requests.
Precise Authorization: Access to resources and command execution should be tightly controlled to prevent misuse.
### 4. Encrypting Communications:
Using SSL/TLS: To protect data transmitted between the client and server, encrypt ZeroMQ communications using SSL/TLS.
### 5. Error Handling and Logging:
Limiting Error Information: Avoid providing excessive details in error messages to clients to prevent revealing sensitive information about the system.
Monitoring and Logging: Carefully log server activities and use this information to identify and respond to security threats.
### 6. Running the Server in an Isolated Environment:
Using Containers: Running the server in isolated environments such as Docker can enhance security and prevent the impact of potentially malicious commands.
### 7. Regular Updates:
Maintenance and Updates: Ensure that all dependencies and libraries used are up-to-date to protect against known vulnerabilities.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
