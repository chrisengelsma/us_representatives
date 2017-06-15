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


postal = {'ALABAMA': 'AL',
          'ALASKA': 'AK',
          'ARIZONA': 'AZ',
          'ARKANSAS': 'AR',
          'CALIFORNIA': 'CA',
          'COLORADO': 'CO',
          'CONNECTICUT': 'CT',
          'DELAWARE': 'DE',
          'FLORIDA': 'FL',
          'GEORGIA': 'GA',
          'HAWAII': 'HI',
          'IDAHO': 'ID',
          'ILLINOIS': 'IL',
          'INDIANA': 'IN',
          'IOWA': 'IA',
          'KANSAS': 'KS',
          'KENTUCKY': 'KY',
          'LOUISIANA': 'LA',
          'MAINE': 'ME',
          'MARYLAND': 'MD',
          'MASSACHUSETTS': 'MA',
          'MICHIGAN': 'MI',
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
          'OHIO': 'OH',
          'OKLAHOMA': 'OK',
          'OREGON': 'OR',
          'PENNSYLVANIA': 'PA',
          'RHODE ISLAND': 'RI',
          'SOUTH CAROLINA': 'SC',
          'SOUTH DAKOTA': 'SD',
          'TENNESSEE': 'TN',
          'TEXAS': 'TX',
          'UTAH': 'UT',
          'VERMONT': 'VT',
          'VIRGINIA': 'VA',
          'WASHINGTON': 'WA',
          'WEST VIRGINIA': 'WV',
          'WISCONSIN': 'WI',
          'WYOMING': 'WY'}
