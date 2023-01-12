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

class energyWb(Workbench):
    def __init__(self):
        self.__class__.Icon=FreeCAD.getUserAppDataDir()+"Mod/EnergyWB/resources/icons/"+'main_icon.png'
        self.__class__.MenuText="Energy Workbench"
        self.__class__.ToolTip="My Energy Workbench. Test it!"
        return

    def Initialize(self) :
        "This function is executed when FreeCAD starts"
        from PySide import QtCore, QtGui
        # -------------------------------------------------------------------- #
        from scripts import basic
       
        cmdlist = [ "importSurfaces"]
        self.appendToolbar(
            str(QtCore.QT_TRANSLATE_NOOP("EnergyTools","EnergyTools")),cmdlist
        )
        self.appendMenu(
            str(QtCore.QT_TRANSLATE_NOOP("Energy", "Energy")), cmdlist
        )
        Log ('Loading Geometry module... done\n')
        
    def GetClassName(self):
        return "Gui::PythonWorkbench"

# The workbench is added
Gui.addWorkbench(energyWb())
