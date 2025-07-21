# Fleetview
Visualize container workload distribution between docker (swarm, standalone) nodes

## Background
I manage my Docker Swarm cluster and standalone nodes from a singel ansible script and was missing a nice webpage to view the distribution and loadbalancing of workloads between the Docker nodes. 
Using SSH to extract the information from each node with the same dedicated user that run the ansible work.
This is not intended to replace monitoring of services but to give a quick overview of your entire estate. (very usful when running multiple clusters or several standalone Nodes)  

## Features:
- Show what docker containers is running on what node
- Show status of the Container
- Show Container uptime
- Filter on status
- Supports both standalone Docker (docker compose) and Docker swarm
  
## Screenshot:

![Screenshot](./Screenshot.png)

## ToDo:
- Default to dark mode
- Add Uptime for each Node
- Add CPU and memory utilization for each Node
- ??? 
