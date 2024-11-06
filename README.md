# mm-scheduling-service
Implements a microservice for managing meeting creation, scheduling, and participant availability for the Meeting Match application.

As of right now, this supports full CRUD for two models: Event and Availability. Anyone can view either of these models, but a user must be authenticated to create one. Additionally, a user must be authenticated AND be the owner of the Event or the Availability in order to edit it.
