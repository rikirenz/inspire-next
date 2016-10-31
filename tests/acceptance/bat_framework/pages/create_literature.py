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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def go_to():
    Arsenic().get(os.environ['SERVER_NAME'] + '/submit/literature/create')


def write_conference(conference_title):
    _skip_import_data()
    return Arsenic().write_in_autocomplete_field('conf_name', conference_title)


def write_journal_title(journal_title):
    _skip_import_data()
    return Arsenic().write_in_autocomplete_field('journal_title', journal_title)


def write_affilation(affilation):
    _skip_import_data()
    return Arsenic().write_in_autocomplete_field('authors-0-affiliation', affilation)


def write_arxiv_id(arxiv_id):
    Arsenic().find_element_by_id('arxiv_id').clear()
    Arsenic().find_element_by_id('arxiv_id').send_keys(arxiv_id)
    Arsenic().find_element_by_id('arxiv_id').send_keys(Keys.TAB)
    return WebDriverWait(Arsenic(), 10).until(EC.presence_of_element_located((By.ID, 'state-arxiv_id'))).text


def write_doi_id(doi):
    Arsenic().find_element_by_id('doi').clear()
    Arsenic().find_element_by_id('doi').send_keys(doi)
    Arsenic().find_element_by_id('doi').send_keys(Keys.TAB)
    return WebDriverWait(Arsenic(), 10).until(EC.presence_of_element_located((By.ID, 'state-doi'))).text


def submit_arxiv_id(arxiv_id):
    Arsenic().find_element_by_id('arxiv_id').send_keys(arxiv_id)
    Arsenic().find_element_by_id('importData').click()
    WebDriverWait(Arsenic(), 20).until(EC.visibility_of_element_located((By.ID, 'acceptData'))).click()
    WebDriverWait(Arsenic(), 10).until(EC.visibility_of_element_located((By.ID, 'arxiv_id')))

    return {
        'doi': Arsenic().find_element_by_id('doi').get_attribute('value'),
        'year': Arsenic().find_element_by_id('year').get_attribute('value'),
        'issue': Arsenic().find_element_by_id('issue').get_attribute('value'),
        'title': Arsenic().find_element_by_id('title').get_attribute('value'),
        'volume': Arsenic().find_element_by_id('volume').get_attribute('value'),
        'abstract': Arsenic().find_element_by_id('abstract').get_attribute('value'),
        'author': Arsenic().find_element_by_id('authors-0-name').get_attribute('value'),
        'journal': Arsenic().find_element_by_id('journal_title').get_attribute('value'),
        'page-range': Arsenic().find_element_by_id('page_range_article_id').get_attribute('value')
        }


def submit_doi_id(doi_id):
    Arsenic().find_element_by_id('doi').send_keys(doi_id)
    Arsenic().find_element_by_id('importData').click()
    WebDriverWait(Arsenic(), 20).until(EC.visibility_of_element_located((By.ID, 'acceptData'))).click()
    WebDriverWait(Arsenic(), 10).until(EC.visibility_of_element_located((By.ID, 'doi')))

    return {
        'year': Arsenic().find_element_by_id('year').get_attribute('value'),
        'title': Arsenic().find_element_by_id('title').get_attribute('value'),
        'issue': Arsenic().find_element_by_id('issue').get_attribute('value'),
        'volume': Arsenic().find_element_by_id('volume').get_attribute('value'),
        'journal': Arsenic().find_element_by_id('journal_title').get_attribute('value'),
        'author': Arsenic().find_element_by_id('authors-0-name').get_attribute('value'),
        'author-1': Arsenic().find_element_by_id('authors-1-name').get_attribute('value'),
        'author-2': Arsenic().find_element_by_id('authors-2-name').get_attribute('value'),
        'page-range': Arsenic().find_element_by_id('page_range_article_id').get_attribute('value')
        }


def _skip_import_data():
    Arsenic().hide_title_bar()
    Arsenic().find_element_by_id("skipImportData").click()
    WebDriverWait(Arsenic(), 10).until(EC.text_to_be_present_in_element((By.ID, "form_container"), 'Type of Document'))
    Arsenic().find_element_by_link_text("Conference Information").click()
    Arsenic().show_title_bar()
