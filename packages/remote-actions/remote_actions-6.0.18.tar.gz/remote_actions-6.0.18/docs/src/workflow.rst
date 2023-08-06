Workflow Actions
========================================

Included in the Poplar Forms package are a number of workflow actions that
can be used to generate and send forms to Sage Users, Extender groups, and 
client email addresses.

.. toctree::


Using Workflow Actions
----------------------

The workflow actions included with the package can be used in any workflow
step.  All workflow actions perform the following:

1. Render the form content message template.
2. Use the rendered content to generate the approval form.
3. Obtain the approval form URL and, if necessary, append default values as URL
   parameters.
4. Render and send an email notification to all specified users.

In order to perform these tasks, the actions all accept the following 
parameters::

    Parameter1: Notification Email Template - used to render notification email
                template, inserting the {FORMURL} template variable.
    Parameter2: To list - Sage Users or Extender Groups to notify of the 
                approval.
    Parameter3: Form Content Template - used to render the form content, the 
                subject is used as the page title and the content is displayed
                above the form.  Both plain text and HTML content are 
                supported.
    Parameter4: Button Labels and Progress To steps - a comma separated list of
                button_label=progress_to_stepname pairs.  

HTML Content in Forms
---------------------

HTML can be used in form titles and content.  Only a subset of HTML tags are 
supported :py:data:`~remote_actions.remote_actions_client.ALLOWED_HTML_TAGS`.

To use HTML content in a form, create a message template that represents a
valid HTML page (i.e. begins/ends with ``<html>`` tags and contains a
``<body>``).

The following message template will render the customer name in italics, an
amount in bold, contains a list, and whitespace management::

    <html>
        <head></head>
        <body>
            <p>Customer <i>{IDCUST} {NAMECUST}</i>  
               has requested a change of credit limit 
               from {AMTCRLIMT:2} to 
               <b>{TOVALUE:2}</b>
            </p>

            <br />

            This is a list of things!
            <ul>
            <li>Thing1</li>
            <li>Thing2</li>
            <li>Lorax</li>
            </ul>


            <p>The change was done on {DD}/{MM}/{YYYY} at 
               {HOUR}:{MINUTE}:{SECOND} by {USER}</p>
        </body>
    </html>


