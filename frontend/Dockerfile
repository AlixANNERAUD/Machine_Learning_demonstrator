FROM node:lts-alpine

# Set environment variables
env TSC_COMPILE_ON_ERROR=1
env ESLINT_NO_DEV_ERRORS=1


# Install simple http server for serving static content
RUN npm install -g http-server

# Make the 'app' folder the current working directory
WORKDIR /app

# Copy 'package.json' to install dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy files and folders to the current working directory (i.e. 'app' folder)
COPY . .

# Build app for production with minification
RUN npm run build

EXPOSE 8080
CMD [ "http-server", "dist" ]