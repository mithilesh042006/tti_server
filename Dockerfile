# Use official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose port for Hugging Face Spaces
EXPOSE 7860

# Run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:7860"]