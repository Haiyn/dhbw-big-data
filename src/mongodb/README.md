# dhbw-big-data-mongodb
> The NoSQL MongoDB that stores the final MTG card data for accessing from applications.

# Data Format
> The data definition of all data stored in the database.

Each card is saved as a JSON document in the "Cards" collection. Each document defines following JSON format:

```json
{
  "multiverseid": "[id]",
  "name": "[name]",
  "artist": "[artist]",
  "text": "[text]"
}
```
In some instances, [the multiverseid might be not defined](https://docs.magicthegathering.io/#api_v1cards_list). In this case, the property simply does not exist in the data entry.

An example json with 3 entries is available in [`/src/mongodb/sample_data.json`](/src/mongodb/sample_data.json).

# Development
> All concerns of developing and deploying the MongoDB.

## Initialization & Deployment
The MongoDB is initialized by the [`docker-compose.yml` file](/docker-compose.yml), which defines [`/src/mongodb/init.js`](/src/mongodb/init.js) 
as the entry point. This script creates the database `dhbw-big-data-mongodb` with a user and a collection.

It runs on the default port `27017`.
## Connecting to the MongoDB
To connect to the MongoDB, you can use multiple ways.
> Be aware that you need to authorize yourself as development user 'dev' (password 'dev').

### 1. Connection String

Generally, you can always use the MongoDB connection string
```
mongodb://dev:dev@[host]:27017/dhbw-big-data-mongodb
```
to connect to the database from various applications, whereas `[host]` is the domain name or IP address of where the 
database is running.

### 2. mongo express
A docker container is running on port `8081` with the DBMS mongo-express. Simply connect to 
`[host]:8081` whereas `[host]` is either `localhost` if you're developing locally or the IP address of your server.

### 3. mongo-clients
The package `mongo-clients` can be used to connect to the database via the shell. After installing the package, you can
run the command 
```bash
mongo "mongodb://dev:dev@localhost:27017/dhbw-big-data-mongodb"
```
to connect to the database. 