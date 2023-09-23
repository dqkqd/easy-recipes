FROM node:20-alpine3.17 as build
WORKDIR /frontend
COPY package*.json ./

RUN npm install

COPY ./ .

RUN npm run build

FROM nginx:stable-alpine
RUN mkdir /app
COPY --from=build /frontend/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]
