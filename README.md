# dhbw-big-data
> An application to browse and search for Magic The Gaterhing cards.
> 
> Created with ❤️ as an exam application for the lecture "Big Data" at DHBW Stuttgart.

 ## Getting Started

> How to get the project up and running.

### Requirements
![Docker Version][docker-image]
![Docker compose Version][compose-image]

Docker and docker compose are required to run this application contained in docker containers.

### Deployment
To get the application up and running, follow these steps on your server.

2. Get all needed data
```bash
git clone https://github.com/Haiyn/dhbw-big-data.git && cd dhbw-big-data
```
2. Start docker containers
```bash
docker-compose up -d
```

3. Wait for airflow container to finish initializing. (`docker logs airflow` say "Container startup finished")

4. Run `setup.sh` script:
```bash
sh setup.sh
```

5. Wait for hadoop container to finish initializing. (`docker logs hadoop` say "Container startup finished")

6. Start all services like this: 
```bash
docker exec -it hadoop bash
sudo su hadoop
cd 
start-all.sh 
```

HDFS will be available at `http://[host]:9870`.

Airflow will be available at `http://[host]:8080/admin/`.

The Frontend will be available at `http://[host]:3000`.

Mongo-express will be available at `http://[host]:8081`.

All other components are not reachable from outside of the docker network.


## Technical Documentation
> Documentation about all technical aspects of this project.
### 1. Docker Ecosystem

The docker ecosystem consists of five containers running in the same network. They communicate with each other and most
of them are also reachable from the outside of the docker network. The graphic below shows the ecosystem. Docker containers
are framed in blue color while other components are framed in grey. The arrows into the network are noted with the port 
that the container is reachable under.

![Docker Ecosystem][docker-ecosystem-image]

### [2. Airflow ETL](./src/airflow)
Airflow is used to run automatic jobs to handle everything around creating, updating and transforming raw and final data.
Uses Hadoop and PySpark.

### [3. MongoDB](./src/mongodb)
The MongoDB database offers a document storage for saving the final MTG data.

### [4. Next.js Frontend](./src/frontend)
The React Next.js frontend is used to give the user an interface for interacting with the final data.




<!-- Image definitions -->
[compose-image]: https://img.shields.io/badge/docker_compose-^1.28.4-blue?style=flat-square&logo=docker
[docker-image]: https://img.shields.io/badge/docker-^20.10.03-blue?style=flat-square&logo=docker
[docker-ecosystem-image]: /docs/docker_ecosystem.png