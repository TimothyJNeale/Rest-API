# CONTRIBUTING
Was notes.txt

### Going to add this change to help tracking branches (I'm still a gi newbie)

## macbook
source .venv/bin/activate  

docker build -t flask-smorest-api .
docker run -dp 5005:5000 flask-smorest-api
docker run -dp 5005:5000  -w /app -v "$(pwd):/app" flask-smorest-api

docer file for
FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

docker run -dp 5000:5000  -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run --host 0.0.0.0"

## pc
.venv\Scripts\activate