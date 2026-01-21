
FROM node:20-alpine

# If your `node:20-alpine` variant lacks npm, install it:
RUN apk add --no-cache npm

WORKDIR /app

COPY package.json package-lock.json* ./
# Use `npm ci` only if you actually have a package-lock.json
RUN if [ -f package-lock.json ]; then npm ci --silent; else npm install --silent; fi

COPY . .

EXPOSE 5173

ENV CHOKIDAR_USEPOLLING=true
ENV WATCHPACK_POLLING=true

CMD ["npm", "run", "dev", "--", "--host"]
