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
    Arsenic().get(os.environ['SERVER_NAME'] + '/submit/literature/create')


def submit_journal_article(input_data):
    _skip_import_data()
    Arsenic().hide_title_bar()
    _links_population(input_data)
    _basic_info_population(input_data)
    _journal_conference_population(input_data)
    _references_comment_population(input_data)
    Arsenic().find_element_by_xpath('//div[@id="webdeposit_form_accordion"]/div[4]/span/button').click()
    Arsenic().show_title_bar()
    return WebDriverWait(Arsenic(), 10).until(EC.visibility_of_element_located((By.XPATH, '(//div[@class="alert alert-success alert-form-success"])'))).text


def _links_population(input_data):
    Arsenic().find_element_by_id("url").send_keys(input_data['pdf-1'])
    Arsenic().find_element_by_id("additional_url").send_keys(input_data['pdf-2'])


def _basic_info_population(input_data):
    Arsenic().find_element_by_id("title").send_keys(input_data['title'])
    Select(Arsenic().find_element_by_id("language")).select_by_value(input_data['language'])
    Arsenic().find_element_by_id("title_translation").send_keys(input_data['title_translation'])
    Arsenic().find_element_by_xpath("(//button[@type='button'])[8]").click()
    Arsenic().find_element_by_css_selector("input[type=\"checkbox\"]").click()
    Arsenic().find_element_by_xpath("//input[@value='" + input_data['subject'] + "']").click()
    Arsenic().find_element_by_xpath("(//button[@type='button'])[8]").click()
    Arsenic().find_element_by_id("authors-0-name").send_keys(input_data['author-0'])
    Arsenic().find_element_by_id("authors-0-affiliation").send_keys(input_data['author-0-affiliation'])
    Arsenic().find_element_by_link_text("Add another author").click()
    Arsenic().find_element_by_id("authors-1-name").send_keys(input_data['author-1'])
    Arsenic().find_element_by_id("authors-1-affiliation").send_keys(input_data['author-1-affiliation'])

    try:
        Arsenic().find_element_by_id("collaboration").send_keys(input_data['collaboration'])
    except (ElementNotVisibleException, WebDriverException):
        pass

    Arsenic().find_element_by_id("experiment").send_keys(input_data['exoeriment'])
    Arsenic().find_element_by_id("abstract").send_keys(input_data['abstract'])
    Arsenic().find_element_by_id("report_numbers-0-report_number").send_keys(input_data['report-number-0'])
    Arsenic().find_element_by_link_text("Add another report number").click()
    Arsenic().find_element_by_id("report_numbers-1-report_number").send_keys(input_data['report-number-1'])


def _journal_conference_population(input_data):
    Arsenic().find_element_by_id("journal_title").send_keys(input_data['journal_title'])
    Arsenic().find_element_by_id("volume").send_keys(input_data['volume'])
    Arsenic().find_element_by_id("issue").send_keys(input_data['issue'])
    Arsenic().find_element_by_id("year").send_keys(input_data['year'])
    Arsenic().find_element_by_id("page_range_article_id").send_keys(input_data['page-range-article'])
    WebDriverWait(Arsenic(), 10).until(EC.visibility_of_element_located((By.ID, "conf_name"))).send_keys(input_data['conf-name'])


def _proceedings_population(input_data):
    WebDriverWait(Arsenic(), 10).until(EC.visibility_of_element_located((By.ID, "nonpublic_note"))).send_keys(input_data['non-public-note'])


def _references_comment_population(input_data):
    WebDriverWait(Arsenic(), 10).until(EC.visibility_of_element_located((By.ID, "references"))).send_keys(input_data['references'])
    WebDriverWait(Arsenic(), 10).until(EC.visibility_of_element_located((By.ID, "extra_comments"))).send_keys(input_data['extra-comments'])


def write_pdf_link(pdf_link):
    message_err = ''
    try:
        WebDriverWait(Arsenic(), 5).until(EC.visibility_of_element_located((By.ID, 'url')))
    except (ElementNotVisibleException, WebDriverException):
        _skip_import_data()
    field = WebDriverWait(Arsenic(), 5).until(EC.visibility_of_element_located((By.ID, 'url')))
    field.send_keys(pdf_link)
    Arsenic().hide_title_bar()
    Arsenic().click_with_coordinates('state-group-url', 5, 5)
    try:
        message_err = WebDriverWait(Arsenic(), 10).until(EC.visibility_of_element_located((By.ID, 'state-url'))).text
    except (ElementNotVisibleException, WebDriverException):
        pass
    Arsenic().show_title_bar()
    field.clear()
    return message_err


def write_date_thesis(date_field, error_message_id, date):
    message_err = ''
    try:
        WebDriverWait(Arsenic(), 5).until(EC.visibility_of_element_located((By.ID, date_field)))
    except (ElementNotVisibleException, WebDriverException):
        _skip_import_data()
        _select_thesis()
    field = WebDriverWait(Arsenic(), 5).until(EC.visibility_of_element_located((By.ID, date_field)))
    field.send_keys(date)
    Arsenic().hide_title_bar()
    Arsenic().click_with_coordinates('state-group-supervisors', 5, 5)
    try:
        message_err = WebDriverWait(Arsenic(), 5).until(EC.visibility_of_element_located((By.ID, error_message_id))).text
    except (ElementNotVisibleException, WebDriverException):
        pass
    Arsenic().show_title_bar()
    field.clear()
    return message_err


def write_institution_thesis(institution):
    _skip_import_data()
    _select_thesis()
    WebDriverWait(Arsenic(), 5).until(EC.visibility_of_element_located((By.ID, 'supervisors-0-affiliation')))
    return Arsenic().write_in_autocomplete_field('supervisors-0-affiliation', institution)


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
    Arsenic().execute_script("""document.evaluate("//div[@id='webdeposit_form_accordion']/div[3]/div[7]/div[1]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE,null).singleNodeValue.click()""")
    Arsenic().execute_script("""document.evaluate("//div[@id='webdeposit_form_accordion']/div[3]/div[8]/div[1]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE,null).singleNodeValue.click()""")
    Arsenic().execute_script("""document.evaluate("//div[@id='webdeposit_form_accordion']/div[3]/div[9]/div[1]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE,null).singleNodeValue.click()""")
    Arsenic().show_title_bar()


def _select_thesis():
    Select(Arsenic().find_element_by_id('type_of_doc')).select_by_value('thesis')
