
FROM node:alpine

# Data preparation
RUN mkdir -p /usr/src/app
ENV PORT 3000

# Dependencies install
# Copy dependency definitions
WORKDIR /usr/src/app
COPY package.json /usr/src/app
COPY yarn.lock /usr/src/app

# Install dependencies
RUN yarn cache clean
RUN yarn install --network-concurrency 1
RUN yarn install

# Copy source files
COPY . /usr/src/app

# Run
RUN yarn build

EXPOSE 3000
CMD [ "yarn", "start" ]