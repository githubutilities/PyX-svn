#!/usr/bin/env python
#
#
# Copyright (C) 2002 J�rg Lehmann <joergl@users.sourceforge.net>
# Copyright (C) 2002 Andr� Wobst <wobsta@users.sourceforge.net>
#
# This file is part of PyX (http://pyx.sourceforge.net/).
#
# PyX is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PyX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyX; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#
# Postscript operators
#

class PSOp:

    """Poscript Operators

    Everything, you can write in a (E)PS file

    """

    def write(self, file):
        """writing into a file is the only routine, a PSOp has to supply"""
        raise NotImplementedError, "cannot call virtual method write()"


#
# Postscript attribute class
#

class PSAttr(PSOp):
    
    """attributes for PSCmds"""
    
    pass


#
# PSCmd class
#

class PSCmd(PSOp):

    """ PSCmd is the base class of all visible elements

    Visible elements, are those, that can be embedded in the Canvas
    and posses a bbox. Furthermore, they can write themselves to
    an open file and to an EPS file
    
    """
    
    def bbox(self):
        raise NotImplementedError, "cannot call virtual method bbox()"


#
# PyX Exception class
#

class PyXExcept(Exception):

    """base class for all PyX Exceptions"""

    pass
