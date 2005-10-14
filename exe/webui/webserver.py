#!/usr/bin/python
# ===========================================================================
# eXe
# Copyright 2004-2005, University of Auckland
#
# This module is for the TwiSteD web server.
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

"""
WebServer module
"""

from twisted.internet              import reactor
from twisted.internet.error        import CannotListenError
from nevow                         import appserver
from twisted.web                   import static
from exe.webui.packageredirectpage import PackageRedirectPage
from exe.webui.editorpage          import EditorPage
from exe.webui.aboutpage           import AboutPage

import logging
log = logging.getLogger(__name__)

class WebServer:
    """
    Encapsulates some twisted components to serve
    all webpages, scripts and nevow functionality
    """
    def __init__(self, application):
        """
        Initialize
        """
        self.application = application
        self.config      = application.config
        self.root        = PackageRedirectPage(self)   
        self.editor      = EditorPage(self.root)
        self.about       = AboutPage(self.root)


    def run(self):
        """
        Start serving webpages from the local web server
        """
        log.debug("start web server running")

        # web resources
        webDir = self.config.webDir
        self.root.putChild("images",      static.File(webDir+"/images"))
        self.root.putChild("css",         static.File(webDir+"/css"))   
        self.root.putChild("scripts",     static.File(webDir+"/scripts"))
        self.root.putChild("style",       static.File(webDir+"/style"))
        self.root.putChild("docs",        static.File(webDir+"/docs"))

        # xul resources
        xulDir = self.config.xulDir
        print xulDir
        self.root.putChild("xulscripts",  static.File(xulDir+"/scripts"))
        self.root.putChild("templates",   static.File(xulDir+"/templates"))

        # sub applications
        self.root.putChild("editor",      self.editor)
        self.root.putChild("about",       self.about)

        try:
            reactor.listenTCP(self.config.port, appserver.NevowSite(self.root),
                              interface="127.0.0.1")
        except CannotListenError, exc:
            log.error("Can't listen on interface 127.0.0.1, port %s: %s" % 
                      (self.config.port, unicode(exc)))
        else:
            reactor.run()
