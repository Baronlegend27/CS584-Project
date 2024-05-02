FROM postgres:16.2

# Set environment variables
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD 123
ENV POSTGRES_DB project

# Add the SQL dump file to the Docker image
ADD dump.sql /docker-entrypoint-initdb.d/
