# Use an official Debian base image
FROM debian:latest

# Install build-essential package for C compilation
RUN apt-get update && apt-get install -y build-essential

# Set the working directory inside the container
WORKDIR /app

# Copy the source code into the container
COPY . .

# Compile the C program
RUN gcc -o program main.c

# Set the command to run the compiled program
CMD ["./program"]
