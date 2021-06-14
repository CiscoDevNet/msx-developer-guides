# MSX Tenants

MSX is a multi-tenant system. MSX tenant is key system concept. It came from MSX being the system built for Service Providers.  
Service Provider hosts MSX instance installation. Service Provider offers Services to its Customers through MSX.
MSX is installed with preconfigured Super User. Super User usually creates a Tenant for each Customer. 

**MSX data is segregated by Tenant.**

All data access in the system is centered around tenancy. MSX Users can access data from one or more Tenants.

Tenants can be organized into hierarchy using parent/child relationship.
Tenant can have one Parent Tenant and any number of Child Tenants. There is not limit on number of levels in the hierarchy. 

Answering the following questions will help position your service in MSX:
* Is My Service multi-tenant?
* How do Tenants in My Service map to MSX Tenants? 
* How does My Service align with MSX Tenancy Model? 
