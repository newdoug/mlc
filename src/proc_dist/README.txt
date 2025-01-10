Lightweight distributed processing solution

Custom distributed processing solution somwhat specific to this project.

Machines/Nodes:

* Master:
** Coordinates computation distribution among other nodes
** (Optionally) Runs job manager. This could be given to another load if desired.
* Other nodes: Runs server and job workers

Components:

* Server: Server that runs on remote (or local) machines ready to receive jobs.
* Worker: Code that runs behind server that actually executes jobs and transfers results back to the job manager through the server(?).
* Job manager:
** Usually runs on master node, but doesn't have to.
** Responsible to distributing tasks/jobs to servers and their workers.
** Responsible for receiving task/job results and putting into database.
