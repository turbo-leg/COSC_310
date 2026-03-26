## Okay so this file creates a container that runs our FastAPI application
## It's so we don't have the famous "it works on my machine" problem
## After this file is created we can run the application using docker-compose up --build
## It should start the application on port 8000
## Go to your browser and type http://localhost:8000/docs
FROM python:3.11-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app ./app
COPY users.csv .
COPY menu_items.csv .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]