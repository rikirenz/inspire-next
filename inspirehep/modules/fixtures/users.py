# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Fixtures for users, roles and actions."""

from __future__ import absolute_import, division, print_function

from flask import current_app
from flask_security.utils import hash_password

from invenio_access.models import ActionRoles

from invenio_db import db


def init_users_and_permissions():
    ds = current_app.extensions['invenio-accounts'].datastore
    with db.session.begin_nested():
        superuser_role = ds.create_role(
            name='superuser',
            description='admin with no restrictions'
        )
        cataloger_role = ds.create_role(
            name='cataloger',
            description='users with editing capabilities'
        )
        ds.create_user(
            email='admin@inspirehep.net',
            password=hash_password("123456"),
            active=True,
            roles=[superuser_role]
        )
        ds.create_user(
            email='cataloger@inspirehep.net',
            password=hash_password("123456"),
            active=True,
            roles=[cataloger_role]
        )
        db.session.add(ActionRoles(
            action='superuser-access',
            role=superuser_role
        ))
        db.session.add(ActionRoles(
            action='admin-access',
            role=superuser_role)
        )
        db.session.add(ActionRoles(
            action='workflows-ui-admin-access',
            role=cataloger_role)
        )
        db.session.add(ActionRoles(
            action='admin-holdingpen-authors',
            role=cataloger_role)
        )

    db.session.commit()
