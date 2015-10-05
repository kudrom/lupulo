import os.path

settings = {
        "cwd": "/home/alarm/m3dpi_ui",
        "serial_device": "/dev/ttyACM0",
        "web_server_port": 8080,
        "serial_mock_timeout": 1,
        "data_schemas": {},
        "activate_mongo": False,
        "mongo_host": "localhost",
        "mongo_db": "robots",
}

settings["templates_dir"] = os.path.join(settings["cwd"], "templates")
settings["data_schema"] = os.path.join(settings["cwd"], "data_schema.json")
