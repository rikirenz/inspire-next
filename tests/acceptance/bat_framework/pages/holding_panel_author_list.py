# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2016 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

from __future__ import absolute_import, division, print_function

import os

from bat_framework.arsenic import Arsenic
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException, WebDriverException


def go_to():
    Arsenic().get(os.environ['SERVER_NAME'] + '/holdingpen/list/?workflow_name=Author&is-update=false&size=10&status=HALTED')


def click_first_record():
    WebDriverWait(Arsenic(), 10).until(EC.visibility_of_element_located((By.XPATH, '//a[@class="title ng-binding ng-scope"]'))).click()
    WebDriverWait(Arsenic(), 10).until(EC.visibility_of_element_located((By.XPATH, '(//div[@class="detail-panel"])[1]')))


def load_submission_record(input_data):
    try:
        record = WebDriverWait(Arsenic(), 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="row hp-item ng-scope"][1]'))).text
    except (ElementNotVisibleException, WebDriverException):
        go_to()
        record = load_submission_record(input_data)
    return record
