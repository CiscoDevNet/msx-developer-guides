# How do MSX Users, Tenants, Roles and Permissions Work Together?

MSX Web Portal is backed up by a set of Microservices exposing REST API.  
MSX User gets access token assigned to him when he logs into the Portal.
Consecutive User actions on the Portal use access token when calling MSX APIs. Web Portal User Interface takes user permissions
into account however logic is easier to demonstrate on REST API call.

