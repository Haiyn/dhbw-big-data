# dhbw-big-data-frontend

> A Next.js frontend used to interact with the card data in the MongoDB.

## Technical Details
Next.js is a React framework that offers a built-in API. 

The application uses Rebass as a frontend framework.

This application contains an automatic connection to a MongoDB outlined by the Configuration of the application.
The route `/api/cards` is available to fetch cards from the MongoDB. It can be parameterized with the following 
parameters:
- `multiverseid` An integer that will be matched _exactly_.
- `name` A string that will be matched with all entries _containing_ the string.
- `artist` A string that will be matched with all entries _containing_ the string.

All route calls will return a maximum of 200 cards.

Parameters can be combined with HTTP GET parameters:
```
/api/cards?artist=DaVinci&text=Angel
```

## Development & Deployment

### Set up environment variables

Ensure that a `.env.local` environment file is present at the document root.
By default, these variables should be set as follows:
```
MONGODB_URI=mongodb://dev:dev@127.0.0.1:27017/dhbw-big-data-mongodb
MONGODB_DB=dhbw-big-data-mongodb
```

- `MONGODB_URI` - Your MongoDB connection string. 
- `MONGODB_DB` - The name of the MongoDB database you want to use.

See the [dhbw-big-data-mongodb documentation](/src/mongodb) for more information on these variables.

### Deployment on localhost

To start the application with development features such as live reload, run it with the following commands:
```bash
npm install
npm run dev

# or

yarn install
yarn dev
```

The application will only work with a running MongoDB database to connect to as outlined in the Configuration section. 
Make sure the frontend container is not already running and blocking the same port.

The application will be up and running on [http://localhost:3000](http://localhost:3000).

### Deployment on a server

Simply use the [`docker-compose.yml` file](/docker-compose.yml) to automatically start the docker container which 
contains the latest image of the frontend application. 

The docker-compose file deploys the application as follows:
```bash
yarn build
yarn start
```

The application will be reachable on port `3000` on your servers domain or IP address.

Be aware that the host name changes to the container name `frontend` if youre connecting from within the docker network.