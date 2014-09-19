# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.


from sgtk.platform import Application

import sgtk
import maya.cmds as cmds
import json
import os


class StgkPositionlistExport(Application):
	"""
	The app entry point. This class is responsible for intializing and tearing down
	the application, handle menu registration etc.
	"""
	
	def init_app(self):
		"""
		Called as the application is being initialized
		"""
		if self.context.entity is None:
			raise tank.TankError("Cannot load the Set Frame Range application! "
								 "Your current context does not have an entity (e.g. "
								 "a current Shot, current Asset etc). This app requires "
								 "an entity as part of the context in order to work.")

		self.tk_multi_poslistExport = self.import_module("tk_multi_positionlistExport")
								 
		self.engine.register_command("Export positionlist", self.run_app)
		
	def destroy_app(self):
		self.log_debug("Destroying StgkPositionlistExport")

	def run_app(self):
		"""
		Callback from when the menu is clicked.
		"""		
		print "start"
		message = "Exported positionlist to \n"

		# try:
		print dir(self.tk_multi_poslistExport.positionlistExport)
		path = self.tk_multi_poslistExport.positionlistExport.createPositionlist()
		message += path
		# except:
			# message = "NO POSITIONLIST EXPORTED!"
		print "end"
		
		# present a pyside dialog
		# lazy import so that this script still loads in batch mode
		from tank.platform.qt import QtCore, QtGui
		QtGui.QMessageBox.information(None, "Position List Exported", message)

		
