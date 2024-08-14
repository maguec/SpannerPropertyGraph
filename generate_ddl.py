#! /usr/bin/env python

from models.nodes import *
from models.edges import *
from models.utils import *

if __name__ == "__main__":
    counties = Counties()
    counties.genddl()
