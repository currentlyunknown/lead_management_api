# Lead Management API

This API allows you to create users and leads. Each user has his own leads, which cannot be accessed by another user.

1. Make sure Docker is installed. `docker -v`
2. Build the image with: `docker-compose build`
3. Start the container with: `docker-compose up -d`
4. Once container is running, by default, your app's URL will be:
http://localhost:8008
5. To see the endpoints, go to:
http://localhost:8008/docs
6. To run automatic tests, run:
`docker-compose exec web poetry run python -m pytest`
