# Use an official Python runtime as a parent image, choosing 3.11 since it has precompiled wheels
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
# Note: we add --no-cache-dir to keep the image small
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 5000

# Run the application using gunicorn, which is recommended for production Flask apps
# Or simply run app.py
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
