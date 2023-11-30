Deployment
==========

This application gets deployed (at a minimum) to two environmetns:

Production -
`https://delphi.cmu.edu/{app_name} <https://delphi.cmu.edu/{app_name}>`__

Staging -
`https://staging.delphi.cmu.edu/{app_name} <https://staging.delphi.cmu.edu/{app_name}>`__

Each environment is essentially a bunch of different services all
governed by ``docker-compose``, running across multiple hosts, with
various layering of proxies and load balancers.

Basic workflow
--------------

-  A PR merged to either ``development`` or ``master`` will trigger CI
   to build container images that are then tagged (based on the branch
   name and ":latest" respectively) and stored in our GitHub Packages
   container image repository.
-  CI triggers a webhook that tells the host systems to pull and run new
   container images and restart any services that have been updated.

Control of the deployed environment
-----------------------------------

The environment and secrets used for deployment live in
https://github.com/cmu-delphi/delphi-ansible-web. Any changes to the
environment should be made there and then tested and validated by devops
folks.
