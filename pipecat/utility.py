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

"""Convenience functions for working with data sources."""

from __future__ import absolute_import, division, print_function

import arrow

import pipecat.record


def add_field(source, key, value):
    """Adds a key-value pair to every record returned from a source."""
    for record in source:
        pipecat.record.add_field(record, key, value)
        yield record


def add_timestamp(source, key="timestamp"):
    """Add a timestamp to every record returned from a source."""
    for record in source:
        pipecat.record.add_field(record, key, arrow.utcnow())
        yield record


def trace(source, label=None):
    """Log the behavior of a source for debugging."""
    if label is None:
        label = source

    pipecat.log.debug("%s started" % label)

    try:
        for record in source:
            pipecat.log.debug("%s record %s" % (label, record))
            yield record
    except GeneratorExit:
        pass

    pipecat.log.debug("%s finished" % label)

