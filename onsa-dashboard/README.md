# Provisioning Dashboard test

Dashboard created for provisioning Service Provider services. Such services can be from an Internet link with certain bandwidth to a dedicated network in the MPLS core. 

The dashboard is just a plain front-end where the provisioning team can set up new clients, services and even deploy them in the network. It is obvious that this dashboard interacts with an orchestrator that is able to identify each service, fetch the resources and deploy the services along the backbone and even in the client node.

## App framework

This app is built with React library from Facebook. It provides flexibility such as composition, where you render only the component you want to with a certain logic. The code is in JavaScript.

## Project

The project was build with `npx create-react-app myapp` command where you have some default folders and files.

* `public/`: Where basically the main .html file is located.
* `src/`: Where all your JavaScript code lives.
    * `components/`: Stores all hand-made components.
    * `css/`: Stores all css files. In this case there's only one.
    * `images/`: Every image used should be in here.
    * `middleware/`: Every piece of code that interacts with the outside world. Mainly networking functions.
    * `pages/`: this folder is important. Since in React there's only one real html page and you render components in it in any way you like, you can still have pages where the user navigates. Each page is modeled as a stateful component.
    * `routes/`: This folder stores the routes of the application. In it private and public routes can be found. Public routes do not need any kind of protection in comparison with private routes, where there's a protection (PrivateRoute component gives this functionality).
    * `App.js`: Main application component. Might need to pay attention to it in some cases.

### Environment files

In order for the app to run properly some environment variables should be set in the project. The naming convention provided by React for the env files is the following.

* `.env`: Default
* `.env.local`: Local overrides. **This file is loaded for all environment except test**.
* `.env.development`, `.env.test`, `.env.production`: Environment-specific settings.
* `.env.development.local`, `.env.test.local`, `.env.production.local`:  Local overrides of environment-specific settings.

For developing, the environment files used at the time this documentation was written, are  `.env.development.local`, `.env.production.local`. These environment files **WILL NOT** be uploaded to the project repository. __If any modification in the environment file should be documented in here__.

`.env.development.local`

```
BROWSER=None # Variable for opening browser on application start-up
PORT=3000 # Running port
HOST=localhost # Listening IP
NODE_ENV=development # Environment variable
```


`.env.production.local`

```
BROWSER=None # Variable for opening browser on application start-up
PORT=80 # Running port
HOST=0.0.0.0 # Listening IP
NODE_ENV=production # Environment variable
```

### Docker

This application is dockerized with `docker-compose`.

`docker-compose.yml`
```yaml
version: '3.7'
services:
  dashboard:
    env_file:
      - ./.dash.dev.env
    build: .
    image: "onsa-dash:${TAG}"
    ports:
     - "${PUBLISH}:${EXPOSE}"
    command: npm start
```
`env_file`: this file contains all the variables for the container environment.

Also you can see that there are variables for compose, these are stored in `.env` file at the same level as `docker-compose.yml`. Since React also uses `.env` file as the default environment file, you should **__NOT__** use it for the app environment. You may also want to run the app as a production stand-alone container, so you should create a `.dash.prod.env` file or whatever name you like.

`.env`

```
EXPOSE=3000
PUBLISH=3000
TAG=dev
```

`.dash.dev.env`

```
EXPOSE=3000
```

### Dependencies

Project dependencies are explicit in `package.json`. Whenever a new dependency is added to the project, `npm install` should be run.

To add a new dependency, `npm install -s <dependency>`.

## Future work

In order for the app to grow some points should be considered.

* `react-redux`: If the app continous to grow, the state of an app can be quit messy so there must be an integration with Redux to store and handle the state of the app.
* `graphql`: The code should be as clean as possible and it should not be modified to change random things, such as the title. To solve this a GraphQL server should be running somewhere so that the app can query resources that may change periodically.
* `sass/less`: If CSS continous growing some new technologies like SASS or LESS should be taken into consideration.