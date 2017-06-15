#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bs4
from bs4 import BeautifulSoup
from pprint import pprint
from us_rep.util import *
from us_rep.us_rep import *

base_url = 'https://en.wikipedia.org/wiki/'
url0 = base_url + 'List_of_former_members_of_the_United_States_House_of_Representatives'
url1 = base_url + 'Current_members_of_the_United_States_House_of_Representatives'
letters = [chr(ord('a') + i).upper() for i in range(26)]
name_endings = ['Jr.', 'Sr.', 'II', 'III']


def run():
    reps = [get_former_reps(), get_current_reps()]
    write_to_json(reps, "representatives.json")


def get_current_reps():
    headline('Getting current reps...')
    soup_page = get_soup(url1)
    span = soup_page.find(id='Voting_members_by_state')
    table = span.parent.findNext('table')

    reps = []

    for tr in table.find_all('tr')[1:]:
        tds = tr.find_all('td')
        if len(tds) == 0:
            continue
        if "Vacant" in tds[1]:
            continue
        rep = parse_current_rep(tds)
        reps.append(rep)

    span = soup_page.find(id='Delegates')
    table = span.parent.findNext('table')

    for tr in table.find_all('tr')[1:]:
        tds = tr.find_all('td')
        rep = parse_current_delegate(tds)
        reps.append(rep)

    return reps


def get_former_reps():
    headline('Getting former reps...')
    reps = []
    prev = None
    for l in letters:
        print l, '...',
        url = ''.join([url0, '_(', l, ')'])
        soup_page = get_soup(url)
        table = soup_page.find('table', attrs={"class": "wikitable sortable"})
        if table is not None:
            for tr in table.find_all('tr')[1:]:
                tds = tr.find_all('td')

                if len(tds[0].text.split(' ')) == 1:
                    year_start, year_end = parse_years(tds[0].text)
                    party = reps[-1].terms[0].party
                    state = reps[-1].terms[0].state
                    reps[-1].terms.append(Term(year_start=year_start,
                                               year_end=year_end,
                                               party=party,
                                               state=state))
                else:
                    rep = parse_former_rep(tds)
                    reps.append(rep)
        print len(reps)
    return reps


def parse_current_delegate(tds):
    state = state_abbrev(tds[1].text)
    party = tds[4].text.split('and')[-1]
    year_start = tds[7].text
    term = [Term(year_start=year_start,
                 year_end='',
                 state=state,
                 party=party)]
    name = tds[3].find('span',attrs={"class": "vcard"}).find('a').text
    first_name, middle_name, last_name = parse_name(name)
    return Representative(first_name=first_name,
                          middle_name=middle_name,
                          last_name=last_name,
                          terms=term)


def parse_current_rep(tds):
    state_list = tds[0].text.split(' ')
    if is_int(state_list[-1]):
        state = ' '.join(state_list[:-1])
    elif 'At Large' in tds[0].text:
        state = tds[0].text[:-9]
    else:
        state = tds[0].text

    state = state_abbrev(state)
    party = tds[3].text
    year_start = tds[6].text[:5]
    term = [Term(year_start=year_start,
                 year_end='',
                 state=state,
                 party=party)]
    name = tds[1].find('span',attrs={"class": "vcard"}).find('a').text
    first_name, middle_name, last_name = parse_name(name)

    return Representative(first_name=first_name,
                          middle_name=middle_name,
                          last_name=last_name,
                          terms=term)


def parse_former_rep(tds):
    first_name, middle_name, last_name = parse_name(tds[0].text)
    terms = parse_terms(tds[1].text, tds[3].text, tds[2].text)

    rep = Representative(first_name=first_name,
                         middle_name=middle_name,
                         last_name=last_name,
                         terms=terms)

    return rep


def parse_terms(year_raw, party_raw, states_raw):
    terms = []
    states = None
    parties = parse_parties(party_raw)
    if states_raw is not None:
        states = parse_states(states_raw)
    i = 0
    j = 0
    for term in year_raw.split(u'\n'):
        year_start, year_end = parse_years(term)

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


def parse_years(year_raw):
    years = year_raw.split(u'\u2013')
    year_start = years[0]
    year_end = years[-1]
    return year_start, year_end


def parse_states(states_raw):
    states = states_raw.split(u'\n')
    for i in range(len(states)):
        states[i] = state_abbrev(states[i])
    return states


def parse_parties(party_raw):
    parties = party_raw.split(u'\n')
    for i in range(len(parties)):
        if '"' in parties[i]:
            parties[i] = parties[i-1]
    return parties


def parse_name(name_raw):
    names = name_raw.split(' ')

    first_name = names[0]
    middle_name = names[1]
    last_name = names[-1]

    # Account for Jr., Sr., etc.
    if last_name in name_endings:
        last_name = ' '.join([names[-2], names[-1]])

    if middle_name in last_name:
        middle_name = ''

    return [first_name, middle_name, last_name]
