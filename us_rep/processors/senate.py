#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bs4
from bs4 import BeautifulSoup
from pprint import pprint
from us_rep.util import *
from us_rep.us_rep import *

base_url = 'https://en.wikipedia.org/wiki/'
url0 = base_url + 'List_of_former_United_States_Senators'
url1 = base_url + 'List_of_current_United_States_Senators'
letters = [chr(ord('a') + i).upper() for i in range(26)]
name_endings = ['Jr.', 'Sr.', 'II', 'III']


def run():
    senators = [get_former_senators(), get_current_senators()]
    write_to_json(senators, "senators.json")


def get_current_senators():
    soup_page = get_soup(url1)
    senators = []
    table = soup_page.find(id='Senators').parent.next_sibling.next_sibling
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) == 0:
            continue
        sen = parse_current_senator(tds)
        senators.append(sen)
    return senators


def get_former_senators():
    soup_page = get_soup(url0)
    senators = []
    for l in letters:
        span = soup_page.find(id=l)
        if span is None:
            continue
        table = span.parent.next_sibling.next_sibling
        for tr in table.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) == 0:
                continue

            sen = parse_former_senator(tds)
            senators.append(sen)
    return senators


def parse_current_senator(tds):
    state = state_abbrev(tds[1].text)
    party = tds[5].text
    year_start = tds[9].text.split(' ')[-1]
    year_end = ''
    term = [Term(year_start=year_start,
                 year_end=year_end,
                 state=state,
                 party=party)]
    name = parse_name(tds[4].find('a').text)
    return Senator(first_name=name[0],
                   middle_name=name[1],
                   last_name=name[2],
                   terms=term)


def parse_former_senator(tds):
    name = parse_name(tds[0].text)
    terms = parse_terms(tds[1].text, tds[4].text, tds[3].text)
    sen = Senator(first_name=name[0],
                  middle_name=name[1],
                  last_name=name[2],
                  terms=terms)
    return sen


def parse_terms(year_raw, party_raw, states_raw):
    terms = []
    parties = parse_parties(party_raw)
    states = parse_states(states_raw)
    i = 0
    j = 0
    for term in year_raw.split('\n'):
        years = term.split(u'\u2013')
        year_start = years[0]
        year_end = years[-1]

        party = parties[i]
        if len(parties) > 1:
            i = i + 1

        state = states[j]
        if len(states) > 1:
            j = j + 1

        terms.append(Term(year_start=year_start,
                          year_end=year_end,
                          party=party,
                          state=state))
    return terms


def parse_states(states_raw):
    states = states_raw.split('\n')
    for i in range(len(states)):
        states[i] = state_abbrev(states[i])
    return states


def parse_parties(party_raw):
    parties = party_raw.split('\n')
    for i in range(len(parties)):
        if '"' in parties[i]:
            parties[i] = parties[i-1]
    return parties


def parse_name(text):
    names = text.split(' ')

    first_name = names[0]
    middle_name = names[1]
    last_name = names[-1]

    # Account for Jr., Sr., etc.
    if last_name in name_endings:
        last_name = ' '.join([names[-2], names[-1]])

    if middle_name in last_name:
        middle_name = ''

    return [first_name, middle_name, last_name]

