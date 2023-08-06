Poller
=====================

The poller retrieves completed remote approval forms and applies them to
their respective workflows.

The poller can be run manually or using Process Scheduler. Manual execution is
helpful while testing and setting up the service but Process Scheduler should 
be used in production environments.

Running the Poller with Process Scheduler
-----------------------------------------

The poller is designed to be run in the background as a Task managed by the 
Windows Task Scheduler.  This can be accomplished using Process Scheduler.

Setting Up Process Scheduler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start by creating an email message template that will be sent to an 
administrator in the event of an error in the poller.  

Open the :guilabel:`Process Scheduler --> Setup --> E-Mail Messages` screen. 
Create a new Process Scheduler Email Template, setting all the required fields
and including the details of the errors in the message body.

.. image:: ../images/psched/02_email_message_template.png
   :width: 600px
   :alt: Process Scheduler Email Messages screen.

With a template created, it is time for a new Schedule.  Open the
:guilabel:`Process Scheduler --> Setup --> Schedules` screen. Create a new 
schedule, setting the Schedul ID, description, and email sending parameters.

.. image:: ../images/psched/03_basic_setup.png
   :width: 600px
   :alt: Process Scheduler Schedules screen.

In the Schedules screen, create a new line, Step Number 1, the company for 
which the poller should run, and set the action to :guilabel:`Run Extender
Script`.

.. image:: ../images/psched/04_add_step.png
   :width: 600px
   :alt: Process Scheduler Schedules screen add a line.

Open the line details by selecting :guilabel:`Detail...` for the current line.
Select the :guilabel:`REMOTEACTION.poller` script and save without any parmeters.

.. image:: ../images/psched/05_set_script.png
   :width: 600px
   :alt: Process Scheduler Schedules screen line details.

Setting Up the Windows Scheduled Task
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With the schedule configured in Process Scheduler, a scheduled task must 
be created that can be run automatically in the background.  To create a new
Scheduled Task, start by opening :guilabel:`Start --> Windows Administrative
Tools --> Task Scheduler`.

.. image:: ../images/psched/06_open_task_scheduler.png
   :width: 400px
   :alt: Open the Windows Task Scheduler from the Start menu.

Right click on the :guilabel:`Task Scheduler Library` and select 
:guilabel:`Create Task`.

Start by defining the task name, User to run the task, and allow the task to 
run in the background when the user is not log in.

.. image:: ../images/psched/07_create_task.png
   :width: 600px
   :alt: Set the basic Task options.

Move on to configure the :guilabel:`Triggers`. Create a trigger that will fire
when the machine is started and every 5 minutes thereafter indefinitely.

.. image:: ../images/psched/08_edit_trigger.png
   :width: 600px
   :alt: Configure a trigger to run at startup and a interval thereafter.

Configure the :guilabel:`Action` that will be performed.  Create a new action 
that :guilabel:`Start a program`.  The program to start is 
``OzIntegrityCheck.exe``, located in the ``Sage300\oz6?a\`` folder.  The 
Schedule ID (``REMOTEACTIONPOLL`` in the example) must be provided as 
an argument.

.. image:: ../images/psched/09_edit_action.png
   :width: 600px
   :alt: Configure the Start a Program action and add the schedule as an 
         argument.

Finally, configure a sensible set of options for the task.  The task should
rarely take longer than a minute to run.  In addition to allowing it being run
on demand for testing, it should be stopped automatically if it has run for an
hour and multiple instances should not run in parallel.

.. image:: ../images/psched/10_task_settings.png
   :width: 600px
   :alt: Configure the task settings.

Once the configuration of the task is complete, restart the computer for the
schedule to take effect, or start it manually.

REMOTEACTION.poller
-------------------

.. automodule:: remote_actions.REMOTEACTION.scripts.Poller
    :members:
    :undoc-members:
    :show-inheritance:
