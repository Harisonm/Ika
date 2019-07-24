<h1>Cheat sheet</h1>

# Presentation
Docker allows you to quickly build, test and deploy applications as portable, self-sufficient containers that can virtually run everywhere.

Docker doesn’t remove unused objects such as containers, images, volumes, and networks unless you explicitly tell it to do so. As you work with Docker, you can easily accumulate a large number of unused objects that consume significant disk space and clutter the output produced by the Docker commands.

This guide serves as a “cheat sheet” to help Docker users keep their system organized and to free disk space by removing unused Docker containers, images, volumes, and networks.

# Containers Python

from root path

### docker-compose
```
# Build Docker-compose
docker-compose -f docker/python3_7/docker-compose.yml build

# Up Docker backend
docker-compose -f docker/python3_7/docker-compose.yml up -d

# Show logs of docker-compose
docker-compose -f docker-compose.yml logs

# show procesus status docker-compose
docker-compose ps
```

## Run programme from docker
```
docker exec python_37 python -m module_path
```

# Docker dev part

## Run jupyter Notebook

Depuis la racine du projet

### Build docker-compose
```
docker-compose -f docker/Dev/docker-compose.notebook.yml build
```

### Run docker-compose
```
LOCAL_PATH_NOTEBOOK=./../../notebooks/ docker-compose -f docker/Dev/docker-compose.notebook.yml up -d
```

### Log docker-compose
```
docker-compose -f docker/Dev/docker-compose.notebook.yml logs
```
