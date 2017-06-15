#!/usr/bin/env python
# -*- coding: utf-8 -*-

from us_rep.us_rep import *
import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup


def state_abbrev(state):
    return postal[state.upper()]


def get_soup(url):
    r = requests.get(url)
    html = r.text.encode('utf-8')
    html = html.replace(b'\xEF\xBB\xBF', b'')
    return BeautifulSoup(html, 'html5lib')


def write_to_json(obj, fname):
    print "Saving ", fname, "...",
    with open(fname, 'wb') as outfile:
        json.dump(obj, outfile, cls=CustomEncoder)
    print "done"


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def headline(text):
    print text
    print('='*len(text))


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


postal = {'ALABAMA': 'AL',
          'ALASKA': 'AK',
          'AMERICAN SAMOA': 'AS',
          'ARIZONA': 'AZ',
          'ARKANSAS': 'AR',
          'CALIFORNIA': 'CA',
          'COLORADO': 'CO',
          'CONNECTICUT': 'CT',
          'DAKOTA': 'DT',
          'DISTRICT OF COLUMBIA': 'DC',
          'DELAWARE': 'DE',
          'FLORIDA': 'FL',
          'GEORGIA': 'GA',
          'GUAM': 'GU',
          'HAWAII': 'HI',
          'IDAHO': 'ID',
          'ILLINOIS': 'IL',
          'INDIANA': 'IN',
          'IOWA': 'IA',
          'KANSAS': 'KS',
          'KENTUCKY': 'KY',
          'LOUISIANA': 'LA',
          'MAINE': 'ME',
          'MARSHALL ISLANDS': 'MH',
          'MARYLAND': 'MD',
          'MASSACHUSETTS': 'MA',
          'MICHIGAN': 'MI',
          'MICRONESIA': 'FM',
          'MINNESOTA': 'MN',
          'MISSISSIPPI': 'MS',
          'MISSOURI': 'MO',
          'MONTANA': 'MT',
          'NEBRASKA': 'NE',
          'NEVADA': 'NV',
          'NEW HAMPSHIRE': 'NH',
          'NEW JERSEY': 'NJ',
          'NEW MEXICO': 'NM',
          'NEW YORK': 'NY',
          'NORTH CAROLINA': 'NC',
          'NORTH DAKOTA': 'ND',
          'NORTHERN MARIANA ISLANDS': 'MP',
          'NORTHWEST': 'NW',
          'OHIO': 'OH',
          'OKLAHOMA': 'OK',
          'OREGON': 'OR',
          'ORLEANS': 'OT',
          'PALAU': 'PW',
          'PHILIPPINES': 'PH',
          'PENNSYLVANIA': 'PA',
          'PUERTO RICO': 'PR',
          'RHODE ISLAND': 'RI',
          'SOUTH CAROLINA': 'SC',
          'SOUTH DAKOTA': 'SD',
          'SOUTHWEST': 'SW',
          'TENNESSEE': 'TN',
          'TEXAS': 'TX',
          'UTAH': 'UT',
          'U.S. VIRGIN ISLANDS': 'VI',
          'UNITED STATES VIRGIN ISLANDS': 'VI',
          'VERMONT': 'VT',
          'VIRGINIA': 'VA',
          'WASHINGTON': 'WA',
          'WEST VIRGINIA': 'WV',
          'WISCONSIN': 'WI',
          'WYOMING': 'WY'}
