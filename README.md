# sciQt
This repository contains templates and premade widgets for rapid GUI development for scientific applications. Widgets include:
* Dashboard: a main window widget which communicates with the application backend through Flask.
* UnitEdit: a text box using Pint for behind-the-scenes unit parsing to a base magnitude. For example, if a user enters "10 uV", the textbox will store a base magnitude of 1e-5.
* ParameterTable: a table offering methods to package user-entered parameters can be packaged into a dictionary or pass a dictionary 
  to update the parameters
* DictMenu: a convenience wrapper around Qt's QMenu/QAction system to allow dynamic construction of complex menus through dictionary representation.
* IconButton: a convenience wrapper around Qt's QToolButton class, linking a user-specified function to a clickable icon.
