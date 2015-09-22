import os.path

settings = {
        "cwd": "/home/kudrom/src/m3dpi_ui",
        "serial_device": "/dev/ttyACM0",
        "web_server_port": 8080,
}

settings["templates_dir"] = os.path.join(settings["cwd"], "templates")
