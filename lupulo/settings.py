import os.path


settings = {
    # Current working directory
    "lupulo_cwd": os.path.dirname(os.path.abspath(__file__)),

    # Avoid the testing port 8081 if you are going to run the tests with
    # an instance of the webpage open in a browser
    "web_server_port": 8080,

    # Log settings
    "log_file": "development.log",
    # "log_file": "production.log",
    "redirect_stdout": True,

    # Enable some behaviour for debugging
    "debug": True,

    # Activate the hot notification of layout and data schema
    "activate_inotify": True,

    # Settings for mongodb
    "activate_mongo": False,
    "mongo_host": "localhost",
    "mongo_db": "robots",

    # Sets what listener the backend is using
    "listener": "mock",

    # Settings for the mock listener
    "mock_timeout": 1,
    "mock_ids": 2,

    # Settings for the serial listener
    "serial_device": "/dev/ttyACM0",
}

settings["templates_dir"] = os.path.join(settings["lupulo_cwd"],
                                         "defaults/templates")

settings["data_schema"] = os.path.join(settings["lupulo_cwd"],
                                       "defaults/data_schema.json")

settings["layout"] = os.path.join(settings["lupulo_cwd"],
                                  "defaults/layout.json")
