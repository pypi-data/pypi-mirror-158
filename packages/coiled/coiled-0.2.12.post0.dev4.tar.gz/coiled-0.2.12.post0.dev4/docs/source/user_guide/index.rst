:notoc:

.. _user-guide:

===========
Coiled Docs
===========

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Start Here
   
   aws-cli
   backends
   getting_started
   next_steps

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Cloud Provider Reference

   aws_reference
   gcp_reference
   azure_reference

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Using Coiled

   cluster
   software_environment
   analytics
   performance_reports
   logging
   gpu
   jupyter
   configuration
   teams
   v2

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Guides

   examples
   tutorials/index
   best_practices
   security

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Help

   support
   faq
   troubleshooting/index

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Reference

   quick_reference
   api
   release_notes
   oss-foundations

👋 Welcome to Coiled's documentation!

What is Coiled?
---------------

`Coiled <https://coiled.io>`_ provides cluster-as-a-service functionality to
provision hosted Dask clusters on demand. It takes the DevOps out of data
science and enables data engineers and data scientists to spend more time on
their real job and less time setting up networking, managing fleets of Docker
images, etc.

.. panels::
   :card: border-0
   :container: container-lg pb-3
   :column: col-md-4 col-md-4 col-md-4 p-2
   :body: text-center border-0
   :header: text-center border-0 h4 bg-white
   :footer: border-0 bg-white

   Hosted Dask Clusters
   ^^^^^^^^^^^^^^^^^^^^

   Securely deploy Dask clusters from anywhere you run Python.

   +++

   .. link-button:: cluster
      :type: ref
      :text: Learn more
      :classes: btn-full btn-block stretched-link

   ---


   Software Environments
   ^^^^^^^^^^^^^^^^^^^^^

   Build, manage, and share conda, pip, and Docker environments. Use them
   locally or in the cloud.

   +++

   .. link-button:: software_environment
      :type: ref
      :text: Learn more
      :classes: btn-full btn-block stretched-link

   ---

   Manage Teams & Costs
   ^^^^^^^^^^^^^^^^^^^^

   Manage teams, collaborate, set resource limits, and track costs.

   +++

   .. link-button:: teams
      :type: ref
      :text: Learn more
      :classes: btn-full btn-block stretched-link


Where does Coiled run?
----------------------

You can run Coiled on AWS or GCP in your own :doc:`cloud provider <backends>` account.

.. panels::
   :card: border-0
   :container: container-lg pb-3
   :column: col-md-6 col-md-6 p-2
   :body: text-center border-0
   :header: text-center border-0 h4 bg-white
   :footer: border-0 bg-white

   Use Coiled with AWS
   ^^^^^^^^^^^^^^^^^^^

   .. figure:: images/logo-aws.png
      :width: 35%
      :alt: Use Coiled with Amazon Web Services (AWS)

   +++

   .. link-button:: aws_configure
      :type: ref
      :text: Learn more
      :classes: btn-full btn-block stretched-link

   ---


   Use Coiled with GCP
   ^^^^^^^^^^^^^^^^^^^

   .. figure:: images/logo-gcp.png
      :width: 100%
      :alt: Use Coiled with Google Cloud Platform (GCP)

   +++

   .. link-button:: gcp_configure
      :type: ref
      :text: Learn more
      :classes: btn-full btn-block stretched-link


How Coiled works
----------------

Coiled handles the creation and management of Dask clusters on cloud computing
environments. This process involves your user environment, Coiled Cloud, and a
cloud computing environment.

.. figure:: images/coiled-architecture.png
   :width: 100%
   :alt: Coiled Architecture

   Coiled Architecture (click image to enlarge)

* **User Environment**

  This is where you use the :doc:`Coiled Python package <getting_started>` along
  with your preferred tools to create Dask clusters and submit Dask
  computations. This could be a Jupyter Notebook on your laptop, a Python script
  on a cloud-hosted VM, or Python code within a task in a workflow management
  system.

* **Coiled Cloud**

  `Coiled Cloud <https://cloud.coiled.io/>`_ provides a cluster dashboard that
  you can use to manage clusters, users, teams, software environments, etc.
  Coiled Cloud also handles provisioning the necessary cloud infrastructure for
  your Dask clusters so you don't have to!

* **Cloud Computing Environment**

  This is the cloud environment where Dask clusters will be created and where
  your Dask computations will run. You can configure Coiled to run on AWS or
  GCP.


Coiled at a glance
------------------

.. tabbed:: Create Dask clusters
   :selected:

   Coiled manages Dask clusters and everything you need to scale Python in the
   cloud robustly and easily. Learn more in the
   :doc:`Dask clusters docs <cluster>`.

   .. code-block:: python

      # Launch a cluster with Coiled
      import coiled

      cluster = coiled.Cluster(
          n_workers=5,
          worker_cpu=4,
          worker_memory="16 GiB",
      )

      # Connect Dask to your cluster
      from dask.distributed import Client

      client = Client(cluster)

.. tabbed:: Use custom software environments

   Coiled helps you manage software environments by building Docker images from
   `pip <https://pip.pypa.io/en/stable/>`_ and
   `conda <https://docs.conda.io/en/latest/>`_ environment files for you. Learn
   more in the :doc:`software environment docs <software_environment>`.

   .. code-block:: python

      # Create a custom "ml-env" software environment
      # with the packages you want
      import coiled

      coiled.create_software_environment(
          name="ml-env",
          conda=["dask", "scikit-learn", "xgboost"],
      )

      # Create a Dask cluster which uses your "ml-env"
      # software environment
      cluster = coiled.Cluster(software="ml-env")



Try Coiled
----------

Ready to get started with Coiled? Sign up and create a free account!

.. link-button:: https://cloud.coiled.io
    :type: url
    :text: Sign up for Coiled
    :classes: btn-full btn-block

.. raw:: html

    <script src="https://fast.wistia.com/embed/medias/g4t5ykjyvj.jsonp" async></script><script src="https://fast.wistia.com/assets/external/E-v1.js" async></script><div class="wistia_responsive_padding" style="padding:56.25% 0 0 0;position:relative;"><div class="wistia_responsive_wrapper" style="height:100%;left:0;position:absolute;top:0;width:100%;"><div class="wistia_embed wistia_async_g4t5ykjyvj videoFoam=true" style="height:100%;position:relative;width:100%"><div class="wistia_swatch" style="height:100%;left:0;opacity:0;overflow:hidden;position:absolute;top:0;transition:opacity 200ms;width:100%;"><img src="https://fast.wistia.com/embed/medias/g4t5ykjyvj/swatch" style="filter:blur(5px);height:100%;object-fit:contain;width:100%;" alt="" aria-hidden="true" onload="this.parentNode.style.opacity=1;" /></div></div></div></div>

