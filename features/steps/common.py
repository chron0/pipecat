# Copyright 2014, Sandia Corporation. Under the terms of Contract
# DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government retains certain
# rights in this software.

from behave import *

import numpy
import toyplot.testing


@given(u'a default canvas')
def step_impl(context):
    context.canvas = toyplot.Canvas()


@given(u'a set of cartesian axes')
def step_impl(context):
    context.canvas = toyplot.Canvas()
    context.axes = context.canvas.cartesian()


@given(u'a sample plot')
def step_impl(context):
    context.axes.plot(numpy.sin(numpy.linspace(0, 10)))


@then(u'the visualization should match the {reference} reference image')
def step_impl(context, reference):
    toyplot.testing.assert_canvas_equal(context.canvas, reference)

