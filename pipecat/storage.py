# Copyright 2016 Timothy M. Shead
#
# This file is part of Pipecat.
#
# Pipecat is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pipecat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pipecat.  If not, see <http://www.gnu.org/licenses/>.

"""Functions for storing data.
"""

from __future__ import absolute_import, division, print_function

import collections
import os

import numpy

import pipecat

class Table(object):
    def __init__(self):
        self._columns = collections.OrderedDict()

    def __len__(self):
        for column in self._columns.values():
            return len(column)
        return 0

    def __getitem__(self, key):
        values = self._columns[key]
        if isinstance(values[0], pipecat.quantity):
            values = pipecat.quantity(numpy.array([value.magnitude for value in values]), values[0].units)
        else:
            values = numpy.array(values)
        return values

    def append(self, record):
        for key, value in record.items():
            if key not in self._columns:
                self._columns[key] = []
            self._columns[key].append(value)

    def keys(self):
        return self._columns.keys()

    def items(self):
        return self._columns.items()

    def values(self):
        return self._columns.values()

class Cache(object):
    """Cache records in memory for column-oriented access."""
    def __init__(self, source):
        self._source = source
        self._storage = Table()

    def __iter__(self):
        return self

    def next(self):
        record = self._source.next()
        self._storage.append(record)
        return record

    @property
    def table(self):
        return self._storage

def cache(source):
    """Create an in-memory cache for records.

    Parameters
    ----------
    source: generator, required
        A source of records to be cached.

    Return
    ------
    cache: instance of :class:`pipecat.storage.Cache`.
    """
    return Cache(source)

def csv(source, fobj):
    """Append records to a CSV file."""
    def implementation(source, fobj): # pylint: disable=missing-docstring
        index = None
        fobj.seek(0, os.SEEK_SET)
        for line in fobj:
            index = line.split(",")[0]
        fobj.seek(0, os.SEEK_END)

        if index is not None:
            index = int(index) + 1
        else:
            index = 0

        for record in source:
            for key, value in sorted(record.items()):
                fobj.write("%s,%s,%s\n" % (index, key, value))
            index += 1
            yield record

    if isinstance(fobj, basestring):
        with open(fobj, "a+b") as fobj:
            for record in implementation(source, fobj):
                yield record
    else:
        for record in implementation(source, fobj):
            yield record

