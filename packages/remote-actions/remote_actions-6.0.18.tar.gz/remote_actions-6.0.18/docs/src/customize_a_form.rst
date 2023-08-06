Customize a Form
================

Forms are highly customizable! Many different fields types are supported, 
validations can be applied, and everything in the form template down to the 
field help text and error messages are easily changed.

Each Workflow Action contains a list of form controls and an action map at the
top of the file after the import statements. By customizing the
``form_controls`` the layout, fields, and actions of a form can be customized.

For a detailed walkthough of creating a new action for a custom Sale Price
approval workflow based on the
:py:mod:`~remote_actions.REMOTEACTION.workflow.SendApprovalFormEmail` action
check out the leisurely start guide.

Create a New Workflow Action
----------------------------

The first step to customizing a form is copying one of the existing actions
to a new Workflow action file.  Because workflow actions are stored in the 
database, an existing action file cannot be copied to a new file and edited.

One method of creating and registering new workflow actions is to view the
file contents from the database and copy them into a new file.

1. Open the :guilabel:`Extender --> Setup --> Scripts` screen.
2. Right-click on the script that will be used to build the new action and
   select :guilabel:`View`. The action file contents open in a text editor.
3. In the text editor, select :guilabel:`File --> New`.
4. Copy the contents of the existing action file to the new file.
5. Close the existing file.
6. Save the new file with a unique name.

Customize the Form
------------------

Each workflow action file included with Poplar Forms has a list of form
controls defined at the top of the action file. A form control is a widget that
displays a field in the form. The standard approval form template looks
something like this::
    
    form_controls = [
                        {
                          'name': 'APPROVALCOMMENT',
                          'type': 'textarea',
                          'label': 'Comments',
                          'required': True,
                        }
                    ]

To customize the form, change the contents of the ``form_controls`` variable
to meet your needs.  

Need a form with a comment that uses a text field instead of a text area?
Edit the ``APPROVALCOMMENT`` form control to be of type text::

    form_controls = [
        {
          'name': 'APPROVALCOMMENT',
          'type': 'text',
          'label': 'Comments',
          'required': True,
        }
    ]

Users sometimes need a nudge, if you want to tell users up front that the
comment is required, add some help text to render with the field::

    form_controls = [
        {
          'name': 'APPROVALCOMMENT',
          'type': 'text',
          'label': 'Comments',
          'required': True,
          'help_text': 'Comments are required, please leave one.',
        }
    ]

Because Comments are required, perhaps an initial value is in order to
save time in the best case::

    form_controls = [
        {
          'name': 'APPROVALCOMMENT',
          'type': 'text',
          'label': 'Comments',
          'required': True,
          'help_text': 'Comments are required, please leave one.',
          'initial': 'Approved'
        }
    ]

Adding New Controls
-------------------

Simply define a new element in the ``form_controls`` list to add an additional
control to the form.

What if we need a new form to store the maximum number of widgets that are 
being approved?

.. code-block:: python

    form_controls = [
        {
          'name': 'APPROVALCOMMENT',
          'type': 'text',
          'label': 'Comments',
          'required': True,
          'help_text': 'Comments are required, please leave one.',
          'initial': 'Approved'
        },
        {
          'name': 'MAXWIDGETS',
          'type': 'integer',
          'label': 'Maximum Widgets',
          'required': True,
          'help_text': 'What is the maximum number of widgets being approved?',
          'initial': '5432'
        }
    ]

Where's the Data?
-----------------

Yes but... where does the data from the new field go?  When the 
:py:class:`Poller` applies a form of type ``workflow_approval`` (like this one)
all the fields are set as values in the Workflow itself.  

So in the case described above, in the steps following the approval wait step,
the ``MAXWIDGETS`` value with be set in the Workflow and can be referenced 
as ``{MAXWIDGETS}``.

Progress To Steps and Form Buttons
----------------------------------

The buttons displayed at the bottom of the form, and the step that the workflow
will progress to when they're pressed, are passed as the fourth parameter to 
the workflow action.

They are passed as a comma separated list of button label, progress to step
name pairs.  To render three buttons, :guilabel:`Allow`, :guilabel:`Cancel`,
:guilabel:`Deny` that progress to steps ``Allowed``, ``Canceled``, and
``Denied``, provide the following argument::

    Allow=Allowed,Cancel=Canceled,Deny=Denied

Dynamic Initial Values
----------------------

There are three ways to set initial values in the form. The first is to include
the ``initial`` argument to the form control definition at the top of the
action file::

    form_controls = [
        {
            'name': 'mycontrol',
            ...
            'initial': 'my initial value'
        }
    ]

Using this approach, all users of the form will see the same default value,
regardless of the state of the workflow or the user accessing the form.

To display a value that changes based on the state of the workflow or views
but is the same for all users, change the call to 
:py:func:`~poplar_forms.form_client.create_workflow_approval_form` to include
the initial value as a keyword argument.  

Continuing the ``MAXWIDGETS`` 
example, the initial value can be set to the ``MAXWIDGETS`` value in the 
workflow values by changing the create form call in our custom action::

    
    # Create the form
    try:
        title, content = render_title_and_content_for(e.resolve(e.p3), e)
        form = create_workflow_approval_form(
                            e.wi.viworkih.get("WIID"),
                            form_controls,
                            title,
                            content,
                            actions, 
                            MAXWIDGETS=e.wi.getValue("MAXWIDGETS"))
    except Exception as err:
        showMessageBox("Failed to create approval form: {}".format(err))
        return 1

The final approach is to set a different initial value per user.  This is 
done by customizing the URL parameters in the link sent to each user.
If we wanted to provide a different initial value to each user, we can do so
before the email is sent::

    
    for (username, email_address) in users:
        email = Email()
        email.setTo(email_address)
        if email.load(e.resolve(e.p1)) == False:
            error("Unable to load message template '" + e.p1 + "'")
            return 1

        user_url = "{}?MAXWIDGETS={}&".format(url, user_max_widgets)
        email.replace("FORMURL", user_url)

.. note::
    
    If more than one approach is used to set the initial value of a form 
    control, only one will be applied.

    Initial values set in the form control definition are preferred over
    those set dynamically.  

    Initial values set when creating the workflow form are preferred over
    those set in the URL parameters.
