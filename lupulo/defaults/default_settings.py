import os.path

from lupulo.settings import settings as lupulo_settings

settings = lupulo_settings

# Avoid the testing port 8081 if you are going to run the tests with
# an instance of the webpage open in a browser
settings["web_server_port"] = 8080

# Log settings
settings["log_file"] = "development.log"
settings["redirect_stdout"] = True

# Activate the hot notification of layout and data schema
settings["activate_inotify"] = True

# Settings for mongodb
settings["activate_mongo"] = False
settings["mongo_host"] = "localhost"
settings["mongo_db"] = "robots"

# Sets what listener the backend is using
settings["listener"] = "mock"

# Settings for the mock listener
settings["mock_timeout"] = 1
settings["mock_ids"] = 2

# Settings for the serial listener
settings["serial_device"] = "/dev/ttyACM0"

# Allow executions of settings when startup.tac file is not executed, for
# example in sse_client.py
if 'cwd' in settings:
    settings["templates_dir"] = os.path.join(settings["cwd"], "templates")

    settings["data_schema"] = os.path.join(settings["cwd"], "data_schema.json")

    settings["layout"] = os.path.join(settings["cwd"], "layout.json")
