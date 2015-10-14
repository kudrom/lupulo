Architecture
============

As explained in the introduction, the
Asynchronous output interface: used to push information harvested 
     in the environment by the pololu as soon as it's gathered.
C&C interface: used to command the pololu.

TESTING
In order to properly test the software, the project provides several mocks of
several parts of the backend:

Mock of pololu: an mbed program located in tests/serial_mock_mbed that sends
    a json file through the serial port at different intervals of time.
Mock of the serial listener: a high level software mock written in python that
    publishes information to the web server whenever it's available.

The general idea is to test the serial connection between the pololu and m3dpi_ui
with the mock of the mbed software and to test the logic of the entire project
with the mock of the serial listener.

To run the tests, place the interpreter in the directory containing the
project and type trial m3dpi_ui.tests

