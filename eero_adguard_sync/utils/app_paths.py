from appdata import AppDataPaths


app_paths = AppDataPaths()
if app_paths.require_setup:
    app_paths.setup()
