PyQtGraph's Helper Functions
============================

Simple Data Display Functions
-----------------------------

.. autofunction:: pyqtgraph.plot

.. autofunction:: pyqtgraph.image

.. autofunction:: pyqtgraph.dbg

Color, Pen, and Brush Functions
-------------------------------

Qt uses the classes QColor, QPen, and QBrush to determine how to draw lines and fill shapes. These classes are highly capable but somewhat awkward to use. PyQtGraph offers the functions :func:`~pyqtgraph.mkColor`, :func:`~pyqtgraph.mkPen`, and :func:`~pyqtgraph.mkBrush` to simplify the process of creating these classes. In most cases, however, it will be unnecessary to call these functions directly--any function or method that accepts *pen* or *brush* arguments will make use of these functions for you. For example, the following three lines all have the same effect::

.. code-block:: python

    pg.plot(xdata, ydata, pen='r')
    pg.plot(xdata, ydata, pen=pg.mkPen('r'))
    pg.plot(xdata, ydata, pen=QPen(QColor(255, 0, 0)))

.. autofunction:: pyqtgraph.mkColor

.. autofunction:: pyqtgraph.mkPen

.. autofunction:: pyqtgraph.mkBrush

.. autofunction:: pyqtgraph.hsvColor

.. autofunction:: pyqtgraph.intColor

.. autofunction:: pyqtgraph.CIELabColor

.. autofunction:: pyqtgraph.colorCIELab

.. autofunction:: pyqtgraph.colorDistance

Color Type Aliases
^^^^^^^^^^^^^^^^^^

.. autoattribute:: pyqtgraph.functions.color_like

Data Slicing
------------

.. autofunction:: pyqtgraph.affineSlice

Coordinate Transformation
-------------------------

.. autofunction:: pyqtgraph.transformToArray

.. autofunction:: pyqtgraph.transformCoordinates

.. autofunction:: pyqtgraph.solve3DTransform

.. autofunction:: pyqtgraph.solveBilinearTransform

.. autofunction:: pyqtgraph.invertQTransform

SI Unit Conversion Functions
----------------------------

.. autofunction:: pyqtgraph.siFormat

.. autofunction:: pyqtgraph.siScale

.. autofunction:: pyqtgraph.siEval

.. autofunction:: pyqtgraph.siParse

Image Preparation Functions
---------------------------

.. autofunction:: pyqtgraph.functions.makeARGB

.. autofunction:: pyqtgraph.functions.makeQImage

.. autofunction:: pyqtgraph.functions.applyLookupTable

.. autofunction:: pyqtgraph.functions.rescaleData

.. autofunction:: pyqtgraph.functions.imageToArray

Mesh Generation Functions
-------------------------

.. autofunction:: pyqtgraph.isocurve

.. autofunction:: pyqtgraph.isosurface

Miscellaneous Functions
-----------------------

.. autofunction:: pyqtgraph.eq

.. autofunction:: pyqtgraph.arrayToQPath

.. autofunction:: pyqtgraph.pseudoScatter

.. autofunction:: pyqtgraph.systemInfo

.. autofunction:: pyqtgraph.exit

Legacy Color Helper Functions
-------------------------------

The following helper functions should no longer be used. The functionality that they implement is trivial and it is suggested that the user use the equivalent QColor methods directly.

.. autofunction:: pyqtgraph.colorTuple

.. autofunction:: pyqtgraph.colorStr

.. autofunction:: pyqtgraph.glColor
