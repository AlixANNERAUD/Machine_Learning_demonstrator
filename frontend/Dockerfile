# Build
FROM node:lts-alpine AS build-stage

# Set the working directory
WORKDIR /app

ENV VITE_BACKEND_URL=VITE_BACKEND_URL_PLACEHOLDER

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the files to the working directory
COPY . .

# Build the project
RUN npm run build

# Production
FROM nginx:stable-alpine AS production-stage

ENV APPLICATION_DIRECTORY=/usr/share/nginx/html

# Copy the build files to the nginx server
COPY --from=build-stage /app/dist $APPLICATION_DIRECTORY

# Copy the substitute_environment_variables.sh script to the docker-entrypoint.d directory
COPY --from=build-stage /app/substitute_environment_variables.sh /docker-entrypoint.d/substitute_environment_variables.sh

# Change the permissions of the script
RUN chmod +x /docker-entrypoint.d/substitute_environment_variables.sh

# Expose the port 80
EXPOSE 80

# Start the nginx server
CMD ["nginx", "-g", "daemon off;"]