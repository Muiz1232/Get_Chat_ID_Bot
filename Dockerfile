# Use the Python 3.12 Alpine image as the base
FROM python:3.12-alpine

# Set the working directory
WORKDIR /get-chat-id-bot

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the bot
CMD ["python", "main.py"]
