rd /s /q ".mypy_cache"
rd /s /q ".temp"
rd /s /q ".tox"
rd /s /q "build"
rd /s /q "dist"
rd /s /q ".pytest_cache"
del .coverage
cd src
rd /s /q "log_handler.egg-info"
rd /s /q "logHandler.egg-info"
rd /s /q "my_log_handler.egg-info"