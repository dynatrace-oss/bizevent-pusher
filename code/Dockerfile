# Stage 1: Copy all files into the build-env container
FROM python:3-slim AS build-env
COPY . /app
RUN pip install --no-cache-dir -r /app/requirements.txt
WORKDIR /app

# Stage 2: Use Google distroless and only copy in the app files
FROM gcr.io/distroless/python3

COPY --from=build-env /app /app
# Copy site-packages (which contains the 'requests' module from 'build-env' into the new image)
COPY --from=build-env /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
WORKDIR /app
# Make sure Python knows where to find the 'requests' module
ENV PYTHONPATH=/usr/local/lib/python3.12/site-packages

ENTRYPOINT ["python", "./app.py"]
