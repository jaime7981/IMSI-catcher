import socket
import random
import time

def generate_random_phrase():
    phrases = [
        "Hello, how are you?",
        "What's the weather like today?",
        "Have a great day!",
        "I love programming!",
        "This is a simulated GSM signal."
    ]
    return random.choice(phrases)

def serve_gsm_signal():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set the server address and port
    server_address = ('localhost', 5555)

    # Bind the socket to the server address and port
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)

    print("Server is listening on {}:{}".format(*server_address))

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from {}:{}".format(*client_address))

        try:
            while True:
                # Generate a random phrase
                phrase = generate_random_phrase()

                # Send the phrase as a GSM signal to the client
                client_socket.sendall(phrase.encode())

                # Wait for a short period of time before sending the next phrase
                time.sleep(1)

        except Exception as e:
            print("Error occurred: {}".format(e))

        finally:
            # Close the client socket
            client_socket.close()

if __name__ == '__main__':
    serve_gsm_signal()