FROM node:8.11.1

WORKDIR /scr/frontend

ENV PATH /scr/frontend/node_modules/.bin:$PATH

COPY package.json .
RUN npm install
RUN npm install -g @angular/cli@6.2.9

COPY . .

CMD ["ng", "serve", "--host", "0.0.0.0"]
