FROM surnet/alpine-python-wkhtmltopdf:3.12.1-0.12.6-small

# Set working directory to project folder
WORKDIR /app

# Copy requirements and install Python dependencies
COPY project/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

# Create the media directory first, then copy the file
RUN mkdir -p /app/project/media/application_files
COPY data_files /app/project/media/application_files

# Change to project directory and run
WORKDIR /app/project

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]