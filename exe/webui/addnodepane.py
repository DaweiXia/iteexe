# ===========================================================================
# eXe 
# Copyright 2004-2005, University of Auckland
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# ===========================================================================

import sys
import logging
import gettext
from exe.webui import common
from exe.engine.packagestore import g_packageStore
log = logging.getLogger(__name__)
_   = gettext.gettext


# ===========================================================================
class AddNodePane(object):
    """
    AddNodePane is responsible for creating the XHTML for add nodes links
    """
    def __init__(self, node):
        self.package = None
        self.node = node
        self.url     = ""

    def process(self, request):
        """ 
        Write description
        """
        
        packageName = request.prepath[0]
        self.package = g_packageStore.getPackage(packageName)
        
        if self.package.levelNames[0] in request.args:
            self.package.currentNode = self.package.root.createChild()
            
        if self.package.levelNames[1] in request.args:
            parentId = self.package.currentNode.id[0]
            parentNode = self.package.root.findNode(parentId)
            self.package.currentNode = parentNode.createChild()
            
        if self.package.levelNames[2] in request.args:
            parentId = self.package.currentNode.id[1 : 2]
            parentNode = self.package.root.findNode(parentId)
            self.package.currentNode = parentNode.createChild()
            
            
    def render(self):
        #Returns an XHTML string for viewing this pane
        
        html = common.submitButton("%s", "Add %s")+ "<br/>" 
        html += %(self.package.levelNames[0], self.package.levelNames[0])
        
        if len(self.node.id) < 1:
            html += common.submitButton("%s", "Add %s",False) + "<br/>"
            html += %(self.package.levelNames[1], self.package.levelNames[1])
        else:
            html += common.submitButton("%s", "Add %s") + "<br/>"
            html += %(self.package.levelNames[1], self.package.levelNames[1])
            
        if len(self.node.id) < 2:
            html += common.submitButton("%s", "Add %s",False) + "<br/>"
            html += %(self.package.levelNames[2], self.package.levelNames[2])
        else:
            html += common.submitButton("%s", "Add %s") + "<br/>"    
            html += %(self.package.levelNames[2], self.package.levelNames[2])   
            
        return html
        
        
         


    
# ===========================================================================
