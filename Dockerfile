# Base image for Python environment (replace with a compatible version if needed)
FROM python:3.11-slim



# Set working directory
WORKDIR /app

# Copy project directory and pre-activated virtual environment
COPY . .

# Install project dependencies (assuming requirements.txt is present)
COPY requirements.txt .
RUN pip install -r requirements.txt --verbose --timeout=120

# Expose port (adjust as needed)
EXPOSE 8000

# Command to run the application (replace with your actual command)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
