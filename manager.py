# @Time    : 2019/6/30 20:31
# @Author  : young
from flask_migrate import Migrate

from app import create_app, db

app = create_app("develop")

Migrate(app, db)
