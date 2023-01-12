# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#***************************************************************************
#*   (c) Fernando Castillo Vicencio    castillovicencio@aol.com  2022      *
#*                 https://github.com/fernandocastillovicencio             *
#*                                                                         *
#*   This file is part of the FreeCAD CAx development system.              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   FreeCAD is distributed in the hope that it will be useful,            *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Lesser General Public License for more details.                   *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with FreeCAD; if not, write to the Free Software        *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************/

import PySide
from PySide import QtCore, QtGui
import FreeCAD
import FreeCADGui
import Part
import os

__dir__ = os.path.dirname(__file__)

# FreeCAD Command made with a Python script
def importSurfaces():
    # ------------------------------- Functions ------------------------------ #
    vxname = lambda i: 'vertex'+str(i).zfill(2)
    edname = lambda i: 'edge'+str(i).zfill(2)
    # ----------------------------- Get IDF file ----------------------------- #
    def get_idf_file():
        # ------------------------- a) import library ------------------------ #
        from eppy.modeleditor import IDF
        # ----------------------------- b) names ----------------------------- #
        epfdir = '/media/fernando/hdd3/vboxFiles/files/energyPlus/ExampleFiles/'
        idf_file="1ZoneUncontrolled_win_1.idf"
        # -------------------------- c) set idd file ------------------------- #
        iddfile = epfdir + 'Energy+.idd'
        IDF.setiddname(iddfile)
        # ------------------------- d) get zone name ------------------------- #
        idf = IDF(epfdir+idf_file)
        return idf
    # ------------------------------------------------------------------------ #
    def mkVertices(doc,surfaces):
        # ------------------------- import libraries ------------------------- #
        from eppy.function_helpers import getcoords
        # -------------------------- axis dictionary ------------------------- #
        ax = {0:'x' , 1:'y' , 2:'z'}
        # -------------------- get vertex coordinates -------------------- #
        x = getcoords(surfaces)
            # ---------------------------------------------------------------- #
        for i in range(4):
            # ----------------------- Create vertex ---------------------- #
            cmd = 'doc.addObject( \"Part::Vertex\" , \"'+vxname(i)+'\" )'
            exec(cmd)
            # ---------------------- Set coordinates --------------------- #
            for j in range(3):
                cmd = 'doc.'+vxname(i)+'.'+ax[j].upper()+' = ' + str(x[i][j]*1e3)
                exec(cmd)
    # ------------------------------------------------------------------------ #
    def rmVertices(doc):
        for i in range(4):
            cmd = 'doc.removeObject(\"'+vxname(i)+'\")'
            exec(cmd)        
    # ------------------------------------------------------------------------ #
    def mkEdges(doc):
        for i in range(4):
            # -------------- select the vertices to make an edge ------------- #
            v1 = vxname(i);
            v2 = vxname(i+1) if i<3 else vxname(0)
            # ------------------------- create Edges ------------------------- #
            cmd ='e = Part.makeLine( ' +\
                'doc.'+v1+'.Shape.Vertex1.Point,'+\
                'doc.'+v2+'.Shape.Vertex1.Point'+\
            ')' 
            exec(cmd)
            # ---------------------- add to the document --------------------- #
            cmd =  'doc.addObject(\"Part::Feature\",\"'+\
                edname(i)+'\").Shape = e'
            exec(cmd)
    # ------------------------------------------------------------------------ #
    def rmEdges(doc):
        for i in range(4):
            cmd = 'doc.removeObject(\"'+edname(i)+'\")'
            exec(cmd)
    # ------------------------------------------------------------------------ #
    def mkSurface(doc,surface_name):
        # --------------- Create the surfaces from the n edges --------------- #
        cmd = 'sur=Part.Face(Part.Wire(Part.__sortEdges__(['
        for i in range(4):
            # --------------------------- add edges -------------------------- #
            cmd+='doc.'+edname(i)+'.Shape.Edge1' 
            if i<3: cmd+=','
        cmd += '])))'
        exec(cmd)
        # ------------------ add the surface to the document ----------------- #
        cmd = 'doc.addObject(\"Part::Feature\",\"'+surface_name+'\").Shape=sur'
        exec(cmd)
    # ------------------------------------------------------------------------ #
    def setColorSurf(doc,surface_name,surface_type):
        epcolor = {
            'Wall'      :   ( 0.79687500 , 0.69531250 , 0.39843750 ),
            'Floor'     :   ( 0.55078125 , 0.55078125 , 0.55078125 ),
            'Roof'      :   ( 0.59765625 , 0.29687500 , 0.29687500 ),
            'Shading'   :   ( 0.44531250 , 0.29296875 , 0.60156250 ),
            'Window'    :   ( 0.60546875 , 0.76953125 , 0.78515625 )
        }
        cmd = 'doc.getObject(\"'+surface_name+'\").'+\
            'ViewObject.ShapeColor=' + str(epcolor[surface_type]) 
        exec(cmd)
    # ------------------------------------------------------------------------ #
    def execution(doc,idf):
        # ---------------------------- processing ---------------------------- #
        for surfaces in idf.idfobjects['BuildingSurface:Detailed']:
            # ----------------- get surface names and zone id ---------------- #
            surface_name = surfaces['Name'][6:].replace(' ','_')
            surface_type = surfaces['Surface_Type']
            zone_id = surfaces['Name'][:5].replace(' ','_')
            # ------------------------- make vertices ------------------------ #
            mkVertices(doc,surfaces)
            # -------------------------- Make edges -------------------------- #
            mkEdges(doc)
            # ------------------------ remove vertices ----------------------- #
            rmVertices(doc)
            # ------------------------- Make surfaces ------------------------ #
            mkSurface(doc,surface_name) 
            # ------------------------- remove edges ------------------------- #
            rmEdges(doc)
            # -------------------------- Set colors -------------------------- #
            setColorSurf(doc,surface_name,surface_type)            
    # ------------------------------------------------------------------------ #
    # ---------------------- Select the active document ---------------------- #
    doc = FreeCAD.ActiveDocument
    # ------------------------------- Execution ------------------------------ #
    idf1 = get_idf_file()
    # ------------------------ Execute the importation ----------------------- #
    execution(doc,idf1)
    FreeCADGui.ActiveDocument.ActiveView.fitAll()
# ---------------------------------------------------------------------------- #
# GUI command that links the Python script
class _importSurfacesCmd:
    """Command to create a box"""
    
    def Activated(self):
        # what is done when the command is clicked
        importSurfaces()

    def GetResources(self):
        # icon and command information
        # -------------------------------------------------------------------- #
        MenuText = QtCore.QT_TRANSLATE_NOOP( 'Basic1_Box', 'Box' )
        ToolTip = QtCore.QT_TRANSLATE_NOOP('Basic1_Box', 'Creates a new box')
        return {
            'Pixmap': __dir__ + '/../resources/icons/e2c.svg',
            'MenuText': MenuText,
            'ToolTip': ToolTip
            }

    def IsActive(self):
        # The command will be active if there is an active document
        return not FreeCAD.ActiveDocument is None

FreeCADGui.addCommand('importSurfaces', _importSurfacesCmd())