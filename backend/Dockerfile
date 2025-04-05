FROM public.ecr.aws/lambda/python:3.12

# Install Poetry package manager
RUN pip install poetry

# Copy configuration files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to not create virtual environment (using system Python)
RUN poetry config virtualenvs.create false

# Install project dependencies
RUN poetry install

# Copy application source code to Lambda task root
COPY app/ ${LAMBDA_TASK_ROOT}/app/

# Set the Lambda handler
CMD [ "app.main.handler" ] 