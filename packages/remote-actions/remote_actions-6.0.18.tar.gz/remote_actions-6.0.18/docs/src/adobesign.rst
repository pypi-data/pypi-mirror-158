Adobe Sign Quickstart
============================

This guide provides a detailed walkthrough of connecting Remote Action
to Adobe Sign.

.. note::

    Adobe Sign is supported in Remote Action version 5.1 and newer.

The overall process that needs to be completed to connect Adobe Sign to the
Remote Action service is:

1. Create an account.
2. Create a new API application.
3. Perform the initial configuration in Sage.
4. Complete the OAuth workflow.

Creating an Account
-------------------

Remote Actions will connect to the User's Adobe sign account.  The user must
create an account before a connection can be established.

For demonstration and testing, a free developer account can be used.  All 
agreements created using a demo account have a watermark applied and cannot
be used in production.

To create a new developer account, visit the 
`Adobe Sign Developer Account Sign-Up`_.

.. _Adobe Sign Developer Account Sign-Up: https://acrobat.adobe.com/ca/en/sign/developer-form.html

Creating the API Application
------------------------------

An API Application allows a service, like Remote Actions, to obtain a token
used to act on a user's behalf.  The application must be created and authorized
by the user to obtain tokens.  The authorization can be revoked at any time.

To create an API application, sign in to Adobe Sign and take the following
steps:

1. Once you've signed in, you will be redirected to your dashboard. The
   URL will be in the form ``https://secure.<shard>.adobesign.com/...``. 
   The shard will be a short code like ``na1``, ``eu2``, or ``ap3``. 
   Take note of:

    - Shard:

.. figure:: https://s3.amazonaws.com/dev.expi/content/remote_actions/adobe-sign/02-shard.png
    :width: 400px
    
    The shard for this account is ``na4``.

2. In the navigation column on the left of the screen, expand
   :guilabel:`Adobe Sign API` and open :guilabel:`API Applications`.

3. In the API Applications page, click the :guilabel:`+` icon to create
   a new application.
    
.. figure:: https://s3.amazonaws.com/dev.expi/content/remote_actions/adobe-sign/02-adobe-sign-application-create.png
    :width: 600px

    Click the :guilabel:`+` icon to create a new application.

4. Create a new CUSTOMER API application.

    - Name: remote-action-service-<COMPANY>
    - Description: Remote Action - Intergate with Sage 300 - <COMPANY>
    - Domain: CUSTOMER

.. figure:: https://s3.amazonaws.com/dev.expi/content/remote_actions/adobe-sign/03-adobe-sign-configure-application.png
    :width: 600px
    
    Define a new CUSTOMER API application.

5. Once the application has been created, highlight it and select
   :guilabel:`Configure OAuth`.  
   
.. figure:: https://s3.amazonaws.com/dev.expi/content/remote_actions/adobe-sign/04-adobe-sign-configure-oauth-link.png
    :width: 600px
    
    Highlight the new application to reveal :guilabel:`Configure OAuth` link.

6. Configure OAuth for the application. Take note of:

    - Client ID:
    - Client Secret:

   Set the following values:

    - Redirect URI: https://poplars.dev/adobe-sign-activate.html
    - Enable the following OAuth Scopes with the modifier ``self``:

      - user_read
      - agreement_read
      - agreement_write
      - agreement_send

.. figure:: https://s3.amazonaws.com/dev.expi/content/remote_actions/adobe-sign/05-adobe-sign-configure-oauth.png
    :width: 600px
    
    Record the Client ID and Client Secret, set the scopes for ``self``.

5. In Sage, start 
   :guilabel:`Extender --> Remote Action --> Setup --> Adobe Sign Connect`.

.. figure:: https://s3.amazonaws.com/dev.expi/content/remote_actions/adobe-sign/06-adobe-sign-connect.png
    :width: 600px
    
    Open the Adobe Sign Connect utility to start connecting Remote Action to
    your Adobe Sign account.

6. Fill in the Shard, Client ID, and Client Secret that you noted in the 
   previous steps. Once filled in, the :guilabel:`Authorize` button will 
   be enabled.

.. figure:: https://s3.amazonaws.com/dev.expi/content/remote_actions/adobe-sign/08-adobe-sign-connect-authorize.png
    :width: 400px
    
    Input the Shard, Client ID, and Client Secret recorded in the previous 
    steps.

7. Click the :guilabel:`Authorize` button. A web browser will open, prompt
   you to sign in and authorize the application to connect to Adobe Sign
   on your behalf.

8. After authorizing the application, you will be redirected to the Poplar 
   Development Adobe Sign Connection Confirmation page.  This page will
   display the values required to complete the connection. Take note 
   of:

    - Access Point:
    - Connection Code:

.. figure:: https://s3.amazonaws.com/dev.expi/content/remote_actions/adobe-sign/09-adobe-sign-connect-codes.png
    :width: 600px
    
    The Poplar Development Adobe Sign Connection Confirmation page displays
    the Connection Code and API Access point required to complete the 
    connection.

9. Input the Access Point and Connection Code into the Adobe Sign Connect
   screen in Sage.  Complete the connection by clicking on the 
   :guilabel:`Connect` button.

.. note::
    
    If the access point URL ends with a ``/`` it will automatically
    be removed.

.. figure:: https://s3.amazonaws.com/dev.expi/content/remote_actions/adobe-sign/10-adobe-sign-connect-connect.png
    :width: 400px
    
    When you click :guilabel:`Connect`, the process will be completed and
    a persistent connection established.

10. Once connected, the configuration is complete.

.. figure:: https://s3.amazonaws.com/dev.expi/content/remote_actions/adobe-sign/11-adobe-sign-connect-connected.png
    :width: 400px
    
    When you click :guilabel:`Connect`, the process will be completed and
    a persistent connection established.


