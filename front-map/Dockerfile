FROM node:16
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ARG VUE_APP_API_URL=http://localhost:8100
ENV VUE_APP_API_URL=$VUE_APP_API_URL
RUN npm run build
EXPOSE 8080
CMD ["npm", "run", "serve"]