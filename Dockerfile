# First stage: Build
FROM python:3.11-slim as builder

# Set the working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential

# Install Python dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Second stage: Final image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /Users/Doha/AppData/Roaming/Python/Python311/site-packages/ /Users/Doha/AppData/Roaming/Python/Python311/site-packages/

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
