FROM surnet/alpine-python-wkhtmltopdf:3.12.1-0.12.6-small

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY project/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code and data files
COPY . .

# Command to run your application
CMD ["python", "project/manage.py", "runserver", "0.0.0.0:8000"]