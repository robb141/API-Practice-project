# Use a small official Python image.
# The slim variant keeps the image smaller than the full Python image.
FROM python:3.14-slim

# Prevent Python from writing .pyc files and keep logs visible immediately.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Put all app files inside /app in the container.
WORKDIR /app

# Install only the dependencies needed to run the API.
# Copying requirements first helps Docker reuse this layer when app code changes.
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy the FastAPI application code.
COPY app ./app

# Run the app as a normal user instead of root.
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Document that the app listens on port 8000.
EXPOSE 8000

# Run the API server.
# 0.0.0.0 makes the server reachable from outside the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
