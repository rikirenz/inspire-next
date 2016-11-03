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

import os

from bat_framework.arsenic import Arsenic
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException, WebDriverException
from bat_framework.pages import holding_panel_list


def go_to():
    holding_panel_list.go_to()
    holding_panel_list.click_first_record()

def load_submitted_record(input_data):
    try:
        record = WebDriverWait(Arsenic(), 10).until(EC.visibility_of_element_located((By.XPATH, '(//div[@class="ng-scope"])[2]'))).text
        record += Arsenic().find_element_by_xpath('//p[@class="text-center ng-scope"]').text
        record += Arsenic().find_element_by_xpath('(//div[@class="col-md-9 col-sm-9 col-xs-8 ng-binding"])[1]').text
        record += Arsenic().find_element_by_xpath('(//div[@class="col-md-9 col-sm-9 col-xs-8 ng-binding"])[2]').text
    except (ElementNotVisibleException, WebDriverException):
        go_to()
        record = load_submitted_record(input_data)
    return record


def accept_record():
    Arsenic().find_element_by_xpath('//button[@class="btn btn-warning"]').click()
    return WebDriverWait(Arsenic(), 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="alert ng-scope alert-accept"]'))).text