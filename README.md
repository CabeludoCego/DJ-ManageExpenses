# Documentation

Django Project based on [Cryce Truly's project](https://github.com/CryceTruly/TrulyInexpensible/tree/master).

## Branch: V2 - Django Upgrades

Proposal: Implement changes based on modern Django patterns and features not included in the original project.
Motivation: The author chose a HTML/JS heavy setup, using of HTML forms and inputs, with an Ajax-based search engine. Based on my knowledge, it is possible to implement the same features using Django built-in features, with django forms and queries. 

### Proposal: A web application to manage finances in different currencies, henceforth the name, ManageFinances.

Additional proposals for V2:

1. Forms fully build in django
2. Queries done in Django
3. Analysis to implement more class based views (CBV)
4. Study and identification of other viable Django features to be implemented.

### Resources: Expenses CRUD, Authentication, User Preferences management.

So far, following the project and adding some QoL learned from my previous experiences and newer versions of Django.

### Future Objectives

Add side branches to implement radical changes.
  * 1 - Fully update the model and forms structure to newer standards, including Django forms and crispy forms usage.
  * 2 - Revamp the database structure to add a multi-tenancy layout (same db, users split by 'tenant_id').
  * 2.1 - Soft tryout on the (same db, different schemas).


