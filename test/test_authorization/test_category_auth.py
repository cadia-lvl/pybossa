# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2015 SF Isle of Man Limited
#
# PyBossa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBossa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBossa.  If not, see <http://www.gnu.org/licenses/>.

from default import Test, assert_not_raises
from pybossa.auth import require
from nose.tools import assert_raises
from werkzeug.exceptions import Forbidden, Unauthorized
from mock import patch
from test_authorization import mock_current_user
from factories import CategoryFactory
from pybossa.model.category import Category



class TestProjectAuthorization(Test):

    mock_anonymous = mock_current_user()
    mock_authenticated = mock_current_user(anonymous=False, admin=False, id=2)
    mock_admin = mock_current_user(anonymous=False, admin=True, id=1)


    @patch('pybossa.auth.current_user', new=mock_anonymous)
    def test_anonymous_user_cannot_crud(self):
        """Test anonymous users cannot crud categories"""
        category = CategoryFactory.build()

        assert_raises(Unauthorized, require.ensure_authorized, 'create', category)
        assert_not_raises(Exception, require.ensure_authorized, 'read', category)
        assert_not_raises(Exception, require.ensure_authorized, 'read', Category)
        assert_raises(Unauthorized, require.ensure_authorized, 'update', category)
        assert_raises(Unauthorized, require.ensure_authorized, 'delete', category)


    @patch('pybossa.auth.current_user', new=mock_authenticated)
    def test_authenticated_user_can_crud(self):
        """Test authenticated users cannot crud categories"""
        category = CategoryFactory.build()

        assert_raises(Forbidden, require.ensure_authorized, 'create', category)
        assert_not_raises(Exception, require.ensure_authorized, 'read', category)
        assert_not_raises(Exception, require.ensure_authorized, 'read', Category)
        assert_raises(Forbidden, require.ensure_authorized, 'update', category)
        assert_raises(Forbidden, require.ensure_authorized, 'delete', category)


    @patch('pybossa.auth.current_user', new=mock_admin)
    def test_admin_can_crud(self):
        """Test admin user can crud categories"""
        category = CategoryFactory.build()

        assert_not_raises(Forbidden, require.ensure_authorized, 'create', category)
        assert_not_raises(Forbidden, require.ensure_authorized, 'read', category)
        assert_not_raises(Forbidden, require.ensure_authorized, 'read', Category)
        assert_not_raises(Forbidden, require.ensure_authorized, 'update', category)
        assert_not_raises(Forbidden, require.ensure_authorized, 'delete', category)
