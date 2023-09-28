# Laboratory work Nr.1

**Online car parts shopping platform (ex: Ebay, MegaZip)**

## Assess Application Suitability

#### Scalability
Microservices allow you to scale individual components of your online grocery store independently based on demand. For example, during holiday seasons or special promotions, the order processing service can be scaled up without affecting other services.
#### Faster Development: 
Microservices enable faster development cycles as each component can be developed independently by different teams.
#### Improved Fault Isolation: 
Isolating different services means that if one service fails, it won't necessarily bring down the entire system. This leads to improved fault tolerance and better user experience.
#### Technological Diversity: 
Different services can use the most appropriate technology stack for their specific task, which can lead to improved performance and efficiency.
#### Continuous Deployment: 
Microservices facilitate continuous deployment and delivery, allowing you to release updates and features more frequently without disrupting the entire system.
#### Adaptability to Changing Requirements: 
Online car parts shops often face changing customer preferences and marketed items.
#### Third-Party Integration:
Microservices make it easier to integrate with third-party services and APIs, such as payment gateways or mapping services, which is crucial for a seamless user experience.

## Define Service Boundaries
![image](https://github.com/valik261201/PAD/blob/main/LAB_1/Screenshot%202023-09-28%20125327.png)

#### Shopping Cart Service
- Building the bill
- Sending data to the Catalog service
- Saving/getting data from Shopping Cart DB

#### Catalog Service
- Showing grocery catalog
- Updating Catalog
- Sending data to the Shopping Cart service 
- Saving/getting data from Catalog DB

## Choose Technology Stack and Communication Patterns
- Gateway: JS
- Microservices & DB: - Python, Flask, PostgreSQL, Non-relational DB
- Communication: RESTful APIs

## Design Data Management

### Shopping Cart Service

**POST /create_order**
> JSON 
```
request: { 
           "item" : "oil_pump",
           "item_id" : "a1",
           "quantity" : 5,
          }
```
> Response
> JSON
```
payload: { 
           "bill_id" : 1,
           "item" : "oil_pump",
           "idtem_id" : "a1"
           "quantity" : 5,
           "price" : 360
          }
```

### Catlog Service
**GET /show_catalog**
> JSON 
```
request: {"show_catalog" : True}
```
> Response
> JSON
```
payload: { 
           "oil_pump": {
            "item_id" : "a1"
            "quantity" : 26,
            "price" : 360
          },
          "engine": {
            "item_id" : "a2"
            "quantity" : 105,
            "price" : 10200
          },
          "fuel_pump": {
            "item_id" : "a3"
            "quantity" : 10,
            "price" : 200
          },
          "pistons": {
            "item_id" : "a4"
            "quantity" : 200,
            "price" : 500
          }
         }
```

**POST /add_catalog**
> JSON
```
request: {  "item" : "brake pads",
            "item_id" : "a5",
            "quantity" : 100,
            "price" : 125
}
```

**PUT /update_catalog**
> JSON
```
request: {  "item_id" : "a5",
            "quantity" : 50,
            "price" : 130
}
```

## Set Up Deployment and Scaling

**Containerization with Docker:**

- Containerization of Microservices: Each microservice will have its Docker container. 
- Dockerfile: Dockerfiles for each microservice. This file contains instructions to build a Docker image, including the base image, dependencies installation, and application setup.
- Building Docker Images: Using the Dockerfile to build Docker images for each microservice. 

**Container Orchestration:**
- Kubernetes is a good choice for container orchestration. Kubernetes is a powerful tool for managing Docker containers in a production environment. It provides features like automated scaling, load balancing, and rolling updates.

OR

- Docker Compose (for Development): While Kubernetes is excellent for production, Docker Compose is useful for local development and testing. It allows you to define and run multi-container applications using a single YAML file.

**Deployment:**

Continuous Integration/Continuous Deployment (CI/CD): Implementation of a CI/CD pipeline to automate the deployment process. (Tools like Jenkins, GitLab CI/CD, or Travis CI)

**Scaling:**

- Horizontal Scaling: Microservices can be independently scaled horizontally to handle increased load. Kubernetes, for example, provides auto-scaling capabilities based on metrics like CPU utilization and incoming traffic.
- Load Balancing: Using load balancers to distribute traffic evenly among multiple instances of the same microservice. Kubernetes has built-in load-balancing features and also can be used with external load balancers like AWS Elastic Load Balancing or Nginx.