# ---- Estágio 1: build da aplicação Vue ----
FROM node:22-alpine AS build

WORKDIR /app

# A URL da API é injetada em tempo de build (Vite embute em import.meta.env)
ARG VITE_API_URL=http://localhost:8000/api
ENV VITE_API_URL=$VITE_API_URL

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# ---- Estágio 2: servir os arquivos estáticos com Nginx ----
FROM nginx:1.27-alpine AS serve

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
