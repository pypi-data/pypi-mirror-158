Handler Setup
============================

Newer versions of Remote Action require that at least one handler is setup. 
Handlers take actions on completed forms.  Custom handlers can be developed to
take new actions, such as creating an object, in place of the default form 
approval.

There is one supported handler:

1. Workflow Approval Form handler: advance workflows based on form contents.

.. note::

   If no handlers are setup, you will see errors like this in the log::

        WARNING  Poller type not configured or failed to start.

   In cases like this, manually setup the default handler.

Configuring a Handler
---------------------

Handlers are configured by adding entries to the ``Remote Action Handlers``
custom table.  Each entry has a ``Form Type``, which matches the type sent to
Fleeting Forms and will be used to dispatch completed forms to the correct 
handlers.For each type, a dotted class path is provided to the code that will
do the handling.

If you're working with workflow approval forms, you need exactly one entry:

- Form Type: ``workflow_approval``
- Handler Class: ``remote_actions.handlers.workflow_approval.WorkflowApprovalFormHandler``

.. note:: 

   The default handler should be added at the time Remote Action is installed. 
   If you're upgrading from a previous version you will have to add it by hand.

   If the default handler is not configured it is always safe to add it.
