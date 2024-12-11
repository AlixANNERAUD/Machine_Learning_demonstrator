#!/bin/sh

echo "Substituting environment variables..."

# Replace env vars in files served by NGINX
for file in $APPLICATION_DIRECTORY/assets/*.js* $APPLICATION_DIRECTORY/index.html;
do
  sed -i 's|VITE_BACKEND_URL_PLACEHOLDER|'${BACKEND_URL}'|g' $file
  # Your other variables here...
done

# Let container execution proceed
exec "$@"