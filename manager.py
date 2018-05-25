#! /usr/bin/env python
import os
import unittest

from flask_migrate import Migrate, MigrateCommand

import tests
from app import create_app, db
from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

# def test():
#     """Run the unit tests."""
#     test = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)
