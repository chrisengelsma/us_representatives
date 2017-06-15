#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Representative(object):

    def __init__(self,
                 first_name=None,
                 middle_name=None,
                 last_name=None,
                 terms=None):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.terms = terms

