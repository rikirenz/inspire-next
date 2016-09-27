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
from time import sleep

from selenium.webdriver.common.keys import Keys


def test_literature_create_article_manually(selenium, login):
    selenium.get(os.environ['SERVER_NAME'] + '/submit/literature/create')
    selenium.find_element_by_id("skipImportData").click()
    Select(selenium.find_element_by_id("type_of_doc")).select_by_value("article")
    _links_population(selenium)
    _basic_info_population(selenium)
    _journal_population(selenium)
    _conference_population(selenium)
    _proceedings_population(selenium)
    _references_population(selenium)
    _comments_population(selenium)

def test_literature_create_thesis_manually(selenium, login):
    selenium.get(os.environ['SERVER_NAME'] + '/submit/literature/create')
    selenium.find_element_by_id("skipImportData").click()
    Select(selenium.find_element_by_id("type_of_doc")).select_by_value("article")
    _links_population(selenium)
    _basic_info_population(selenium)
    _thesis_population(selenium)
    _references_population(selenium)
    _comments_population(selenium)


def _links_population(selenium):
    selenium.find_element_by_id("url").send_keys("http://www.pdf995.com/samples/pdf.pdf")
    selenium.find_element_by_id("additional_url").send_keys("http://www.pdf995.com/samples/pdf.pdf")


def _basic_info_population(selenium):
    # Title
    selenium.find_element_by_id("title").send_keys("My Title For Test")
    # Language
    Select(selenium.find_element_by_id("language")).select_by_value("rus")
    # Title translation
    selenium.find_element_by_id("title_translation").send_keys("My Title was in Russian")
    # Subjects
    selenium.find_element_by_xpath("(//button[@type='button'])[8]").click()
    selenium.find_element_by_css_selector("input[type=\"checkbox\"]").click()
    selenium.find_element_by_xpath("//input[@value='Computing']").click()
    # Author 1
    selenium.find_element_by_id("authors-0-name").send_keys("Mister White")
    selenium.find_element_by_id("authors-0-affiliation").send_keys("Wisconsin U., Madison")
    # Author 2
    selenium.find_element_by_link_text("Add another author").click()
    selenium.find_element_by_id("authors-1-name").send_keys("Mister Brown")
    selenium.find_element_by_id("authors-1-affiliation").send_keys("CERN")
    # Collaboration (avaliable only for articles)
    try:
        selenium.find_element_by_id("collaboration").send_keys("This is a collaboration")
    except NoSuchElementException:
        pass
    # Experiment
    selenium.find_element_by_id("experiment").send_keys("This is a collaboration")
    # Abstract
    selenium.find_element_by_id("abstract").send_keys("Lorem ipsum dolor sit amet, consetetur sadipscing elitr.")
    # Report Numbers
    selenium.find_element_by_id("report_numbers-0-report_number").send_keys("100")
    selenium.find_element_by_link_text("Add another report number").click()
    selenium.find_element_by_id("report_numbers-1-report_number").send_keys("101")


def _thesis_population(selenium):
    selenium.find_element_by_id("supervisors-0-name").send_keys("Mister Yellow")
    selenium.find_element_by_id("supervisors-0-affiliation").send_keys("2016-09-27")
    selenium.find_element_by_id("thesis_date").send_keys("2016-09-27")
    selenium.find_element_by_id("defense_date").send_keys("CERN")
    Select(selenium.find_element_by_id("degree_type")).select_by_value("Bachelor")
    selenium.find_element_by_id("institution").send_keys("Wisconsin U., Madison")


def _journal_population(selenium):
    selenium.find_element_by_id("journal_title").send_keys("europ")
    selenium.find_element_by_id("volume").send_keys("Volume")
    selenium.find_element_by_id("issue").send_keys("issue")
    selenium.find_element_by_id("year").send_keys("2014")
    selenium.find_element_by_id("page_range_article_id").send_keys("100-110")


def _conference_population(selenium):
    selenium.find_element_by_id("conf_name").send_keys("This Conference")


def _proceedings_population(selenium):
    selenium.find_element_by_id("nonpublic_note").send_keys("This proceedings")


def _references_population(selenium):
    selenium.find_element_by_id("references").send_keys("references")


def _comments_population(selenium):
    selenium.find_element_by_id("extra_comments").send_keys("comments about the document")
