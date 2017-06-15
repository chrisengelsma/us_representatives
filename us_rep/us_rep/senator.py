#!/usr/bin/env python
# -*- coding: utf-8 -*-
from us_rep import *


class Senator(Representative):

    def __init__(self,
                 first_name=None,
                 middle_name=None,
                 last_name=None,
                 terms=None):

        Representative.__init__(self,
                                first_name,
                                middle_name,
                                last_name,
                                terms)
