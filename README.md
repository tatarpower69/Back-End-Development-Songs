# Back-End-Development-Songs

Flask REST API with MongoDB persistence when MONGO_URI is configured. This is an independent capstone implementation; compare API contracts with the course lab before submission.

## Run locally

    python -m pip install -r requirements.txt
    python app.py

The service listens on port 5002. Set MONGO_URI=mongodb://localhost:27017 to use a running MongoDB instance. Without MONGO_URI the service uses in-memory demo data.

## API

- GET /health
- GET /songs and GET /song
- GET /song/<id>
- POST /song (title, artist, lyrics)
- PUT /song/<id>
- DELETE /song/<id>

## Docker

    docker build -t capstone-songs .
    docker run --rm -p 5002:5002 capstone-songs

Use the multi-service Docker Compose package for MongoDB and the Django frontend. No cloud deployment is claimed by this README.
