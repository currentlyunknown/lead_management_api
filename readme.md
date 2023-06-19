# Lead Management API

Make sure Docker is installed.
- docker -v

If not, install it with:
- pip install docker

To start the app, run:
- docker-compose build
- docker-compose up -d

Once running, by default, your app's URL will be:
http://localhost:8008

To test the endpoints, go to:
http://localhost:8008/docs

To run automatic tests, run:
- docker-compose exec web poetry run python -m pytest
