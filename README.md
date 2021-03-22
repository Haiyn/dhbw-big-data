# dhbw-big-data
> An application to browse and search for Magic The Gaterhing cards.
> 
> Created with ❤️ as an exam application for the lecture "Big Data" at DHBW Stuttgart.

## Structure
The repository is structured in a way to represent the docker container ecosystem of this application.

See the following READMEs to learn more about its components.

### [1. Airflow ETL](./src/airflow/README.md)
Airflow is used to run automatic jobs to handle everything around creating, updating and transforming raw and final data.

### [2. Hive Server](./src/hive/README.md)
The hive server handles the raw data fetching and final data transformation for later storage.

### [3. MongoDB](./src/mongodb/README.md)
The MongoDB database offers a key-value storage for saving the final MTG data.

### [4. Next.js Frontend](./src/frontend/README.md)
The React Next.js frontend is used to give the user an interface for interacting with the final data.

## Getting Started

### Requirements
![Docker Version][docker-image]
![Docker compose Version][compose-image]

Docker and docker compose are required to run this application contained in docker containers.

### Setup
To get the application up and running, simply execute the `docker-compose.yml` file in a terminal.

```bash
docker-compose up
```

<!-- Image definitions -->
[compose-image]: https://img.shields.io/badge/docker_compose-^1.28.4-blue?style=flat-square&logo=docker
[docker-image]: https://img.shields.io/badge/docker-^20.10.03-blue?style=flat-square&logo=docker
