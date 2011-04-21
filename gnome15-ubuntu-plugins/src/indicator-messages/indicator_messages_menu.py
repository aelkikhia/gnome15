#!/usr/bin/env python
from dbus.exceptions import DBusException
 
#        +-----------------------------------------------------------------------------+
#        | GPL                                                                         |
#        +-----------------------------------------------------------------------------+
#        | Copyright (c) Brett Smith <tanktarta@blueyonder.co.uk>                      |
#        |                                                                             |
#        | This program is free software; you can redistribute it and/or               |
#        | modify it under the terms of the GNU General Public License                 |
#        | as published by the Free Software Foundation; either version 2              |
#        | of the License, or (at your option) any later version.                      |
#        |                                                                             |
#        | This program is distributed in the hope that it will be useful,             |
#        | but WITHOUT ANY WARRANTY; without even the implied warranty of              |
#        | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               |
#        | GNU General Public License for more details.                                |
#        |                                                                             |
#        | You should have received a copy of the GNU General Public License           |
#        | along with this program; if not, write to the Free Software                 |
#        | Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. |
#        +-----------------------------------------------------------------------------+

'''
Specialisation of the DBUSMenu module, specifically for the Indicator Messages 
message. This will show waiting messages from applications such as Evolution,
Empathy, Pidgin, Gwibber and others
'''
 
import dbus
import gnome15.dbusmenu as dbusmenu

from lxml import etree

'''
Indicator Messages  DBUSMenu property names
'''

APP_RUNNING = "app-running"
INDICATOR_LABEL = "indicator-label"
INDICATOR_ICON = "indicator-icon"
RIGHT_SIDE_TEXT = "right-side-text"

'''
Indicator Messages DBUSMenu types
'''
TYPE_APPLICATION_ITEM = "application-item"
TYPE_INDICATOR_ITEM = "indicator-item"
TYPE_SEPARATOR = "separator"
TYPE_ROOT = "root"


class IndicatorMessagesMenuItem(dbusmenu.DBUSMenuItem):
    def __init__(self, id, properties, menu):
        dbusmenu.DBUSMenuItem.__init__(self, id, properties, menu)
        
    def set_properties(self, properties):
        dbusmenu.DBUSMenuItem.set_properties(self, properties)        
        self.type = self.properties[dbusmenu.TYPE] if dbusmenu.TYPE in self.properties else TYPE_ROOT
        if self.type == TYPE_INDICATOR_ITEM and INDICATOR_LABEL in self.properties:
            self.label = self.properties[INDICATOR_LABEL]
        if self.type == TYPE_INDICATOR_ITEM:
            self.icon = self.properties[INDICATOR_ICON] if INDICATOR_ICON in self.properties else None
        
    def get_right_side_text(self):
        return self.properties[RIGHT_SIDE_TEXT] if RIGHT_SIDE_TEXT in self.properties else None
        
    def is_app_running(self):
        return APP_RUNNING in self.properties and self.properties[APP_RUNNING]
        
    def get_type(self):
        return self.properties[dbusmenu.TYPE] if dbusmenu.TYPE in self.properties else None

class IndicatorMessagesMenu(dbusmenu.DBUSMenu):
    
    
    def __init__(self, session_bus, on_change = None):
        try:
            dbusmenu.DBUSMenu.__init__(self, session_bus, "org.ayatana.indicator.messages", "/org/ayatana/indicator/messages/menu", "org.ayatana.dbusmenu", on_change, False)
        except DBusException as dbe:
            dbusmenu.DBUSMenu.__init__(self, session_bus, "com.canonical.indicator.messages", "/com/canonical/indicator/messages/menu", "com.canonical.dbusmenu", on_change, True)

    def create_item(self, id, properties):
        return IndicatorMessagesMenuItem(id, properties, self)