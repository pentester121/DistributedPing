import socketio
import requests
import os
import subprocess
import platform
import socket

# Configure client details
location = "Lorestan"
isp = "Irancell"

# Connect to the server
sio = socketio.Client()

@sio.event
def connect():
    print('Connected to the server')

@sio.event
def new_task(data):
    task_id = data['task_id']
    host = data['host']
    task_type = data['task_type']
    
    # Perform the task based on the type
    result = ""
    
    if task_type == "ping":
        result = ping_host(host)
    elif task_type == "http":
        result = check_http(host)
    elif task_type == "tcp":
        result = check_tcp(host)
    elif task_type == "udp":
        result = check_udp(host)

    # Send result back to the server
    sio.emit('task_result', {
        'task_id': task_id,
        'client_id': sio.sid,
        'location': location,
        'isp': isp,
        'result': result
    })

def ping_host(host):
    try:
        os_type = platform.system()
        if os_type == "Linux" or os_type == "Darwin":
            command = ["ping", "-c", "4", host]
        elif os_type == "Windows":
            command = ["ping", "-n", "4", host]
        else:
            return f"Unsupported OS: {os_type}"

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return f"Ping failed: {result.stderr}"

        return result.stdout
    except Exception as e:
        return f"Ping command error: {str(e)}"

def check_http(host):
    try:
        response = requests.get(f"http://{host}")
        return f"HTTP {response.status_code} - {response.reason}"
    except Exception as e:
        return f"HTTP request error: {str(e)}"

def check_tcp(host):
    try:
        host, port = host.split(':')
        port = int(port)
        with socket.create_connection((host, port), timeout=10) as sock:
            return f"TCP connection to {host}:{port} successful"
    except Exception as e:
        return f"TCP connection error: {str(e)}"

def check_udp(host):
    try:
        host, port = host.split(':')
        port = int(port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(10)  # Set timeout for receiving response
        message = b'Test'

        # Send the UDP packet
        sock.sendto(message, (host, port))

        try:
            data, server = sock.recvfrom(4096)
            return f"UDP response from {host}:{port} - {data}"
        except socket.timeout:
            return f"UDP packet sent to {host}:{port}, but no response within timeout"
        except socket.error as e:
            return f"UDP socket error: {str(e)}"
    except Exception as e:
        return f"UDP error: {str(e)}"

# Connect to the server
sio.connect('http://217.196.107.35:5000')  # Replace 'your-server-ip' with your server's IP or domain
sio.wait()

