Changelog
=========

lupulo follows the semantic versioning without distinction between even and odd
numbers of major or minor releases.

[0.2.0] 20/11/2015
------------------

Second release of a stable version of the framework which for the first time has
all the functionalities required to build a functional realtime web page.

#. Loader mechanism to allow dynamic listeners
#. Fully functional templates abstraction
#. Static files can be loaded from the project's directory
#. Asynchronous template rendering
#. Custom urls with support for RESTful interfaces
#. Debug web page
#. Enhanced sse_client
#. Dynamic controllers for the frontend
#. Alerts functions in the frontend
#. Proper licensing

[0.1.0] 05/11/2015
------------------

First release of a stable version of the framework which adds the following
features:

#. Asynchronous data link between the backend and the frontend.
#. First API of both the frontend and backend to allow an easy extension of the
   framework.
#. Layout mechanism to describe the web page in JSON format.
#. Data schema mechanism to describe the data the device is sending to the
   backend in JSON format.
#. Hot change of the layout and data schema both in the frontend and backend.
#. Extensible listener mechanism to connect the device to the backend.
#. Mock listener.
#. Serial listener.
#. Extensible widget mechanism to populate the web page.
#. Multiple line widget.
#. Accessors mechanism to allow a decouple of the view (widgets) from the data
   schema described in the backend.
#. The information received by the backend from the device can be stored in
   a mongodb host.
#. Logging in the backend.
#. Tested both the backend and the frontend.
#. Updated documentation in ReadTheDocs.
#. Redesign of the installation process to fit that one of pip.
