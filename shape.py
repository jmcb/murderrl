#!/usr/bin/env python
"""
Shape, *a collection of clases and functions relating to Shapes*.

Shapes are a grid representation of ASCII graphics. Each point is denoted by an
x and y co-ordinate, where the co-ordinate 0, 0 is the top-left corner of any
shape. These shapes can be of any size, can be drawn onto each other, combined
into a single canvas, collected, split, sectioned, and iterated over.

See the `Shapes`_ section for ``Shape``, ``Box``, ``Column`` and related
classes.

See the `Collections`_ section for ``ShapeCollection`` and ``ShapeCoord``.

"""
from coord import *
from collections import namedtuple

class ShapeError (Exception):
    """
    A generic Shape-related error.
    """
    pass

class ShapeColumn (object):
    """
    ShapeColumn is merely a reference to a specific column of glyphs in a parent
    Shape class. It's implemented thus to allow swapping of the x and y
    co-ordinates when accessing a Shape as though it were a multi-dimensional
    array.

    Modifying via index (ShapeColumn[1]=None, for instance) will in fact
    modify the Shape.
    """
    def copy (s):
        """
        Returns the actual column object as a list. This column object is a
        copy, and any edits made to it are not reflected in the Shape.
        """
        return []
    def parent (s):
        """
        Returns the Shape to which this column belongs.
        """
        return None
    def col (s):
        """
        Returns the column number that this column is a representation of.
        """
        return -1
    def __str__ (s):
        """
        Returns a string representation of the column, where each glyph is
        followed by a new line.
        """
        return ""
    def __repr__ (s):
        """
        Returns a representation of the column as an object.
        """
        return "<ShapeColumn None: 'None'>"
    def __setitem__ (s, row, value):
        """
        Performs in-place assignation via self.parent()[Coord(self.column, row)]
        = value (roughly). In fact, as the class is a closure, it does none of
        these.

        Provides index-based row access to the column, ie, column[1]="x".

        ``row``   = The row that you wish to assign a value to.
        ``value`` = The glyph you want to place. Either len(``value``) == 1
                    or ``value`` is None must be true for the assignation to
                    be successful.
        """
        pass
    def __getitem__ (s, row):
        """
        Returns the glpyh located at ``row``.

        ``row`` = The row being requested for.
        """
        pass
    def __iter__ (s):
        """
        Provides iteration over the content of the column in the format of:
        tuple(Coord, glyph), where Coord equates to the glyph location in the
        Shape (rather than in this column), and the glyph is the relevant glyph.
        """
        pass

    def __eq__ (s, other):
        if not isinstance(other, ShapeColumn):
            return False
        return s.col() == other.col()
    def __ne__ (s, other):
        if not isinstance(other, ShapeColumn):
            return False
        return s.col() == other.col()
    def __lt__ (s, other):
        if not isinstance(other, ShapeColumn):
            return False
        return s.col() < other.col()
    def __le__ (s, other):
        if not isinstance(other, ShapeColumn):
            return False
        return s.col() <= other.col()
    def __gt__ (s, other):
        if not isinstance(other, ShapeColumn):
            return False
        return s.col() > other.col()
    def __ge__ (s, other):
        if not isinstance(other, ShapeColumn):
            return False
        return s.col() >= other.col()

_ShapeColumn = ShapeColumn

class ShapeRow (object):
    """
    ShapeRow is merely a reference to a specific row of glyphs in a parent Shape
    class. It reflects the implementation of the ShapeColumn which is thus
    implemented to allow swapping x and y co-ordinates when accessing a shape as
    though it were a multi-dimensional list.

    Modifying via index (ShapeRow[1]=None, for instance) will in fact modify the
    Shape.
    """
    def copy (s):
        """
        Returns the actual row object as a list. This row object is a
        copy, and any edits made to it are not reflected in the Shape.
        """
        return []
    def parent (s):
        """
        Returns the Shape to which this row belongs.
        """
        return None
    def row (s):
        """
        Returns the row number that this row is a representation of.
        """
        return -1
    def __str__ (s):
        """
        Returns a string representation of the row.
        """
        return ""
    def __repr__ (s):
        """
        Returns a representation of the row as an object.
        """
        return "<ShapeRow None: 'None'>"
    def __setitem__ (s, column, value):
        """
        Performs in-place assignation via self.parent()[Coord(self.row, column)]
        = value (roughly). In fact, as the class is a closure, it does none of
        these.

        Provides index-based column access to the row, ie, row[1]="x".

        ``column`` = The column that you wish to assign a value to.
        ``value``  = The glyph you want to place. Either len(``value``) == 1
                     or ``value`` is None must be true for the assignation to
                     be successful.
        """
        pass
    def __getitem__ (s, column):
        """
        Returns the glpyh located at ``column``.

        ``column`` = The row being requested for.
        """
        pass
    def __iter__ (s):
        """
        Provides iteration over the content of the row in the format of:
        tuple(Coord, glyph), where Coord equates to the glyph location in the
        Shape (rather than in this row), and the glyph is the relevant glyph.
        """
        pass

    def __eq__ (s, other):
        if not isinstance(other, ShapeRow):
            return False
        return s.row() == other.row()
    def __ne__ (s, other):
        if not isinstance(other, ShapeRow):
            return False
        return s.row() == other.row()
    def __lt__ (s, other):
        if not isinstance(other, ShapeRow):
            return False
        return s.row() < other.row()
    def __le__ (s, other):
        if not isinstance(other, ShapeRow):
            return False
        return s.row() <= other.row()
    def __gt__ (s, other):
        if not isinstance(other, ShapeRow):
            return False
        return s.row() > other.row()
    def __ge__ (s, other):
        if not isinstance(other, ShapeRow):
            return False
        return s.row() >= other.row()

_ShapeRow = ShapeRow

class ShapeCoord (namedtuple("ShapeCoord", "shape coord")):
    """
    A named tuple pair providing ``shape`` and ``coord`` members. This is primarily
    used by the ShapeCollection class.
    """
    pass

class ShapeCollection (object):
    """
    A sorted collection of Shapes and co-ordinates. Can be initiliased from a list
    of ShapeCoords or Shapes. For the latter, these will be wrapped in a ShapeCoord
    using Coord(0, 0) as their co-ordinate.

    You can also ``append`` items, ``pop`` items, assign using ShapeCollection[index]
    notation, and fetch via ShapeCollcetion[index] notation.
    """
    _shapes = None
    def __init__ (self, shapes=None):
        self._shapes = []

        if shapes is not None:
            for shape in shapes:
                if isinstance(shape, Shape):
                    shape = ShapeCoord(item, Coord(0, 0))

                assert isinstance(shape, ShapeCoord)
                self._shapes.append(shape)

        self.sort()

    def combine (self):
        """
        Converts a collection into a single Shape by taking the largest contained
        ShapeCoord (or the top-most ShapeCoord determined by sort) and then drawing
        all other ShapeCoords onto it, using their defined Coords as the offset.

        Doesn't currently provide error checking. Should.
        """
        # We take the largest and work on that, ignoring its coord.
        base = self._shapes[0].shape

        for sc in self._shapes[1:]:
            base.draw_on(sc.shape, sc.coord, False)

        return base

    def sort (self):
        """
        In-place sorting by size!
        """
        self._shapes.sort(cmp=lambda a, b: cmp(b.shape.size(), a.shape.size()))

    def append (self, item, coord=None):
        """
        As with the initialisation function, all Shapes passed in are here
        converted into ShapeCoords, using Coord(0, 0) as their offset. All other
        instances are not allowed.
        """
        if coord is not None:
            item = ShapeCoord(item, coord)
        if isinstance(item, Shape):
            self._shapes.append(ShapeCoord(item, Coord(0, 0)))
        elif isinstance(item, ShapeCoord):
            self._shapes.append(item)
        else:
            assert isinstance(item, ShapeCoord)
        self.sort()

    def pop (self, index=-1):
        """
        Pop index ``index`` item from the collection of ShapeCoords.

        ``index`` = The index in question. *Default -1*.
        """
        item = self._shapes.pop(index)
        self.sort()
        return item

    def __getitem__ (self, item):
        """
        Fetch item index ``item`` from the collection of ShapeCoords after
        performing an in-place sort based on Shape size.

        ``item`` = The item to be fetched.
        """
        self.sort()
        return self._shapes.__getitem__(self, item)

    def __setitem__ (self, item, value):
        """
        Insert ``value`` at ``item``, replacing whatever ShapeCoord is existent
        there. Afterwards, an in-place sort is performed.

        ``item``  = The index the value is to be inserted at.
        ``value`` = The value to be inserted. This is automatically cased
                    from a Shape into a ShapeCoord(Shape, Coord(0, 0)).
                    Otherwise it is assumed to be a ShapeCoord. All other
                    types will cause an error.
        """
        if isinstance(value, Shape):
            value = ShapeCoord(shape, Coord(0, 0))
        assert isinstance(value, ShapeCoord)
        result = self._shapes.__setitem__(self, item, value)
        self.sort()
        return result

    def __iter__ (self):
        """
        Creates an iterator for the ShapeCoords contained within, first
        performing an in-place sort.
        """
        self.sort()
        return iter(self._shapes)

    def __len__ (self):
        """
        Returns the number of ShapeCoords contained within.
        """
        return len(self._shapes)

class Shape (object):
    """
    Shapes consist of a canvas grid (with relative Coords). The shape can be
    anything. Shapes can be drawn onto other shapes and have shapes drawn onto
    them.

    Direct glyph access is provided by Shape[x][y], Shape[Coord(x, y)].

    Row and column access by ``row(number)`` and ``column(number)``. The ShapeRow
    and ShapeColumns respectively returned by these are references to the Shape.
    Modifications made to these will be reflected in the Shape.
    """
    _canvas = None
    def __init__ (self, *args, **kwargs):
        """
        Create a new shape.

        ``sh_list`` = A list (or otherwise iterable) representation of a shape.
                      For example, passing [list("...."), list("....")] will
                      result in a 4x2 shape. If passed a Shape, will copy it and
                      create a new shape. *Default None*.
        ``width``   = The width of the shape. If not 0, and ``sh_list`` has been
                      provided, and the width is greater than the shape instatiated
                      from ``sh_list``, the shape will be normalised to this width
                      and ``fill``. If ``sh_list`` is not provided, the shape
                      will be padded with ``fill``. *Default 0*.
        ``height``  = Likewise with ``width``. *Default 0*.
        ``fill``    = For padding purposes or blank, sized shapes, this character
                      will be used to fill the canvas. *Default None*.
        """
        sh_list, width, height, fill = None, 0, 0, None
        if kwargs:
            sh_list = kwargs.get("sh_list", None)
            width = kwargs.get("width", 0)
            height = kwargs.get("height", 0)
            fill = kwargs.get("fill", None)
        if args:
            # Either sh_list or width
            if len(args) >= 1:
                if isinstance(args[0], list):
                    sh_list = args[0]
                elif isinstance(args[0], int):
                    width = args[0]
                else:
                    raise ShapeError, "Unexpected type '%s' for argument 1 of Shape::__init__. Expected list or int." % type(args[0])

            # Must be width or height (can't have a fill for 0*0 shapes)
            if len(args) >= 2:
                if isinstance(args[1], int):
                    if sh_list is not None:
                        width = args[1]
                    else:
                        height = args[1]
                else:
                    raise ShapeError, "Unexpected type '%s' for argument 2 of Shape::__init__. Expected list or int." % type(args[1])

            # Must be height or fll.
            if len(args) >= 3:
                if isinstance(args[2], int):
                    height = args[2]
                else:
                    fill = args[2]

            # We have an sh_list and a width/height.
            if len(args) >= 4 and sh_list is not None:
                fill = args[3]

            if fill is not None and len(fill) != 1:
                raise ShapeError, "Unexpected size %s for argument 'fill' of Shape::__init__. Expect None or single character, got '%s'." % (len(fill), fill)

            if len(args) >= 4 and sh_list is None:
                raise ShapeError, "Unexpected arguments for Shape::__init__: '%s'." % (', '.join([str(x) for x in args[3:]]))

        self._canvas = []
        if not sh_list:
            for row in xrange(height):
                row = []
                for columnn in xrange(width):
                    row.append(fill)
                self._canvas.append(row)
        else:
            if isinstance(sh_list, Shape):
                sh_list = sh_list._canvas

            for row in sh_list:
                nrow = []
                for column in row:
                    nrow.append(column)
                self._canvas.append(nrow)

            if width != 0 and width > self.width():
                self.normalise(width=width, fill=fill)
            if height != 0 and height > self.height():
                self.normalise(height=height, fill=fill)

    def width (self):
        """
        Returns the smallest width that can contain the largest row of the
        shape. *Note: rows padded with ``None`` are not equivalent in length
        to rows without padding.*
        """
        width = 0
        for row in self._canvas:
            if not row:
                continue
            if len(row) > width:
                width = len(row)
        return width 

    def height (self):
        """
        Returns the smallest height that can contain the largest column of
        the shape. *Note: columns are uniform in size across the shape; as with
        rows, ``None`` padding is counted.*"""
        return len(self._canvas)

    def size (self):
        """
        Returns the smallest box that can contain the shape. *Note: this counts
        padding characters (``None``) as normal glyphs. Thus, it is only
        possible to have varying lengths of rows, with the 'gap' being
        represented on the right side of the object.*
        """
        return (self.width(), self.height())

    def column (self, column):
        """
        Returns a ShapeColumn containing all the glyphs in ``column``. See the
        ShapeColumn (closure) class definition for more information.

        ``column`` = The column to return. Required.
        """
        class ShapeColumn (_ShapeColumn):
            __doc__ = _ShapeColumn.__doc__
            def copy (s):
                col = []
                for row in self._canvas:
                    col.append(row[column])
                return col
            copy.__doc__ = _ShapeColumn.copy.__doc__
            def parent (s):
                return self
            parent.__doc__ = _ShapeColumn.parent.__doc__
            def col (s):
                return column
            col.__doc__ = _ShapeColumn.col.__doc__
            def __str__ (s):
                return '\n'.join(str(x) for x in s.copy())
            __str__.__doc__ = _ShapeColumn.__str__.__doc__
            def __repr__ (s):
                return "<ShapeColumn %s: '%s'>" % (column, str(s.copy()))
            __repr__.__doc__ = _ShapeColumn.__str__.__doc__
            def __setitem__ (s, row, value):
                self._canvas[row][column] = value
            __setitem__.__doc__ = _ShapeColumn.__setitem__.__doc__
            def __getitem__ (s, row):
                return self._canvas[row][column]
            __getitem__.__doc__ = _ShapeColumn.__getitem__.__doc__
            def __iter__ (s):
                for i in xrange(self.height()):
                    yield (Coord(column, i), self._canvas[i][column])
            __iter__.__doc__ = _ShapeColumn.__iter__.__doc__

        return ShapeColumn()

    def row (self, row):
        """
        Returns a ShapeRow containing all the glyphs in ``row``. See the
        ShapeRow (closure) class definition for more information.

        ``row`` = The row to return. Required.
        """
        class ShapeRow (_ShapeRow):
            __doc__ = _ShapeRow.__doc__
            def copy (s):
                nrow = []
                for col in self._canvas[row]:
                    nrow.append(col)
                return nrow
            copy.__doc__ = _ShapeRow.copy.__doc__
            def parent (s):
                return self
            parent.__doc__ = _ShapeRow.parent.__doc__
            def row (s):
                return row
            def __str__ (s):
                return str(''.join([str(x) for x in s.copy()]))
            def __repr__ (s):
                return "<ShapeRow %s: '%s'>" % (row, self._canvas[row])
            def __setitem__ (s, column, value):
                self._canvas[row][column] = value
            def __getitem__ (s, column):
                return self._canvas[row][column]
            def __iter__ (s):
                for i in xrange(len(self._canvas[row])):
                    return (Coord(i, row), self._canvas[row][i])

        return ShapeRow()

    def normalise (self, width=None, height=None, fill=None):
        """
        Extend either the width, the height, or both, of a Shape to the relevant
        value, using the provided fill value.

        ``width``  = The width to which the Shape should be extended. This
                     integer value should be greater than the current width
                     of the Shape, or None to perform no width normalisation.
                     *Default None*.
        ``height`` = The height to which the Shape should be extended. As per
                     ``width`` above. *Default None*.
        ``fill``   = The fill character which should be used when extending
                     rows and columns. *Default None*.
        """
        assert width is None or isinstance(width, int)
        assert height is None or isinstance(height, int)

        if width is not None and width > self.size()[0]:
            raise ShapeError, "can't normalise to less than maximum width."

        if height is not None and height > self.size()[1]:
            raise ShapeError, "can't normalise to less than maximum height."

        if fill is not None and len(fill) != 1:
            raise ShapeError, "can't normalise with character '%s'." % fill

        if width:
            for i in xrange(len(self._canvas)):
                while len(self._canvas[i]) < width:
                    self._canvas[i].append(fill)
        if height:
            while len(self._canvas) < height:
                new_row = []
                if width:
                    while len(new_row) < width:
                        new_row.append(fill)
                self._canvas.append(new_row)

    def trim (self, width=None, height=None, trim_left=False, trim_top=False):
        """
        The opposite of normalise in that it reduces the size of a Shape to the
        relevant width or height provided. For reducing width, it can remove
        columns from the right (default) or the left of the shape. For reducing
        height, it can remove rows from the bottom (default) or the top of the
        shape.

        ``width``     = As per normalise, the number of columns to reduce the
                        shape to. Note: this is not the number of columns to
                        remove. *Default None*.
        ``height``    = As per width, only regarding rows.
        ``trim_left`` = Instead remove columns from the left of the shape.
                        *Default False*.
        ``trim_top``  = Instead remove rows from the top of the shape. *Default
                        False*.
        """
        assert trim_left == False or trim_left == True
        assert trim_top == False or trim_top == True

        assert width is None or isinstance(width, int)
        assert height is None or isinstance(height, int)

        if width is not None:
            if trim_left:
                pop = 0
            else:
                pop = -1
            for i in xrange(len(self._canvas)):
                while len(self._canvas[i]) > width:
                    self._canvas[i].pop(pop)

        if height is not None:
            if trim_top:
                pop = 0
            else:
                pop = -1
            while len(self._canvas) > height:
                self._canvas.pop(pop)

    def draw_on (self, shape, offset=Coord(0, 0), check_conflict=True, conflict_except=False):
        """
        Attempt to draw Shape instance ``shape`` on top of self, starting at
        offset ``offset``. Conflict checking is enable by default (ie, it will
        only draw glyphs from ``shape`` onto self if the relevant co-ordinate is
        None), but by default it will simply ignore errors.

        ``shape``           = The shape which will be drawn upon this one. It is
                              presumed that this shape can be contained by self.
                              *Required*.
        ``offset``          = The co-ordinates to begin drawing at (ie, starting with
                              the top left corner of ``shape`` (0, 0), it will begin
                              drawing from here). *Default 0, 0*.
        ``check_conflict``  = Check for conflict before drawing. If true, it
                              will only copy a glyph from ``shape`` onto self if
                              self contains None at that location. *Default
                              True*.
        ``conflict_except`` = If true, will raise a ShapeError upon conflicts.
                              *Default False*.
        """
        assert isinstance(shape, Shape)
        assert (offset+shape.size()) <= self.size()
        for xy, char in shape:
            nxy = xy+offset
            if check_conflict and self[nxy] != None:
                if conflict_except:
                    raise ShapeError, "Tried to blit foreign '%s' onto '%s' at %s!" % (char, self[nxy], nxy)
                else:
                    continue
            self[nxy] = char

    def section (self, section_start, section_stop=None):
        """
        Return a new Shape containing within it the content of the current shape
        from ``section_start`` to ``section_stop``.

        ``section_start`` = The top left co-ordinates of the rectangle. If
                            ``section_stop`` has not been provided, it will be
                            assumed that the section should instead consist of
                            Coord(0, 0) to ``section_stop``.
        ``section_stop``  = The bottom right co-ordinates of the rectangle. See
                            note regarding ``section_start``. *Default None*.
        """
        if section_stop is None:
            section_stop = section_start
            section_start = Coord(0, 0)

        assert section_start < section_stop

        offset = section_stop - section_start

        new_shape = Shape(offset.x, offset.y)
        for coord in RectangleIterator(section_start, section_stop):
            new_shape[coord-section_start] = self[coord]

        return new_shape

    def __iter__ (self):
        """
        Provide an iterator that returns (Coord(x, y), self[x][y]) for each
        glyph within the Shape.
        """
        for rownum in xrange(len(self._canvas)):
            for colnum in xrange(len(self._canvas[rownum])):
                yield (Coord(colnum, rownum), self._canvas[rownum][colnum])

    def __getitem__ (self, item):
        """
        Return either a glyph (if ``item`` is a Coord), or a column (if ``item``
        is an integer). Does **not** support slicing!

        ``item`` = Either a Coord, in which case we return the actual item, or
                   an "x" axis integer. The latter will return a ShapeColumn
                   object that references the column.
        """
        if isinstance(item, Coord):
            return self._canvas[item.y][item.x]
        elif isinstance(item, slice):
            raise Exception, "Do not slice Shape!"
        else:
            return self.column(item)

    def __setitem__ (self, item, value):
        """
        Alter the glyph at ``item`` by replacing with ``value``. Does **not**
        support slicing.

        ``item``  = A co-ordinate, in which case we perform direct assignation
                    of ``value`` to ``item``. The syntax of Shape[x][y] will not
                    actually be parsed by this function. Instead, it is parsed
                    as Shape.column(x)[y].
        ``value`` = Either None, a single-character string, or a list, instance
                    of Shape or its subclass, Column. If passed a 1*x Shape it
                    will attempt to draw the Shape on top of itself (without
                    checking for conflict).
        """
        assert (value is None) or (isinstance(value, list) or isinstance(value, Shape) or isinstance(value, Column)) or (len(value) == 1)
        if isinstance(item, Coord):
            self._canvas[item.y][item.x] = value
        elif isinstance(item, slice):
            raise ShapeError, "Cannot slice Shape!"
        elif isinstance(item, int):
            if isinstance(value, list):
                value = Column(value)
            elif isinstance(value, Shape):
                value = Column(value)
            else:
                raise ShapeError, "Invalid type '%s' for assignation to %s." % (type(value), item)
            self.draw_on(value, Coord(item, 0), False, False)

    def __len__ (self):
        return self.width()

    def __repr__ (self):
        return "<Shape width=%s,height=%s>" % self.size()

    def __str__ (self):
        """
        Translate a Shape into a string. None values are replaced with " ", and
        new lines ("\\n") are inserted at the end of each row.
        """
        result = ""
        for rownum, row in enumerate(self._canvas):
            for column in row:
                if column is None:
                    result += " "
                else:
                    result += column
            if rownum < len(self._canvas)-1:
                result += "\n"
        return result

class Box (Shape):
    """
    A rectangular Shape that provides borders and perimeter access.

    """
    def __init__ (self, width, height, border=1, fill=None, border_fill=None):
        """
        Create a box
        .
        ``width``       = How many characters wide the box should be.
        ``height``      = How many characters tall the box should be.
        ``border``      = The size of border to place. *Default 1*.
        ``fill``        = The fill character of the box. *Default None*.
        ``border_fill`` = The character to use when generating the border which
                          is drawn on top of the fill character (regardless of
                          conflicts).
        """
        self.border = border
        Shape.__init__(self, width, height, fill)
        for c in self.perimeter():
            self[c] = border_fill

    def perimeter (self):
        """
        Returns an iterator of Coords corresponding to the perimeter of the box,
        specifically the border define when initialising the box. If
        ``self.border`` == 0 then will return nothing.
        """
        if self.border < 1:
            return

        w, h = self.size()

        # Top section.
        for x in xrange(w):
            for y in xrange(self.border):
                yield Coord(x, y)

        # Sides!
        for x in xrange(self.border):
            for y in xrange(self.border, h-self.border):
                yield Coord(x, y)
                yield Coord(w-x-1, y)

        # Bottom section
        for x in xrange(w):
            for y in xrange(h-self.border, h):
                yield Coord(x, y)

class Column (Shape):
    """
    A single-character column of characters.
    """
    def __init__ (self, shape=None, height=None, fill=None):
        """
        Create a column.

        ``shape``  = List of characters (or Shape or ShapeColumn) to fill our
                     column with.
        ``height`` = Height to pad the column to. *Default None*.
        ``fill``   = Padding character to use when padding the column. *Default
                     None*.
        """
        if isinstance(shape, ShapeColumn):
            shape = shape.copy()
        if isinstance(shape, Shape):
            assert shape.width() == 1
            Shape.__init__(self, shape, height=height, fill=fill)
        elif isinstance(shape, int):
            if height is not None:
                fill = height
            Shape.__init__(self, width=1, height=shape, fill=fill)
        elif shape is None:
            if height is None:
                height = 1
            Shape.__init__(self, width=1, height=height, fill=fill)
        else:
            nshape = []
            for column in shape:
                nshape.append([column])
            Shape.__init__(self, nshape, height=height, fill=fill)
