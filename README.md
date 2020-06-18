# Sticker BASNet

This is an HTTP service to generate Stickers from pictures, building on top of the [BASNet HTTP 
service by Cyril Diagne](https://github.com/cyrildiagne/BASNet-http).

# Usage:

The `buildImage.sh` bash script will prepare the dependencies, run pytest tests and build the
Docker image. It will also try to push it to the DockerHub repository for the world to see. 
It should be no surprise to anyone, but it is also what the little Jenkins I run executes when
there is a new commit to master. Poor man's CI at its best!

```bash
./buildImage.sh
```

# Testing

When the docker image is running, simply sending a file as an HTTP POST will return the sticker:

```bash
curl -X POST -F "data=@./input.jpg" http://localhost:8000/ -o output.png
````

# Contributing

Improving test coverage is very welcome. This is meant to be a relatively simple service, so
improvements are well received only inasmuch as the image is kept as simple as it can be.


