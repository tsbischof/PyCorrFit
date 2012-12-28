# -*- coding: utf-8 -*-
""" PyCorrFit
    Paul Müller, Biotec - TU Dresden

    Module tools - selectcurves

    Let the user choose which correlation curves to use.
    Contains wrappers for file import and tools.
    
    Dimensionless representation:
    unit of time        : 1 ms
    unit of inverse time: 10³ /s
    unit of distance    : 100 nm
    unit of Diff.coeff  : 10 µm²/s
    unit of inverse area: 100 /µm²
    unit of inv. volume : 1000 /µm³
"""

import numpy as np
import wx
import wx.lib.plot as plot              # Plotting in wxPython



class Wrapper_Tools(object):
    def __init__(self, parent):
        """
        Wrapper for tools menu. Gets curvedict from parent and starts curve
        selection. See *UserSelectCurves* class.
        """
        # parent is the main frame of PyCorrFit
        self.parent = parent

        ## MYID
        # This ID is given by the parent for an instance of this class
        self.MyID = None
        
        ## Wrapping
        curvedict = self.GetCurvedict()
        self.Selector = UserSelectCurves(parent, curvedict, wrapper=self)
        # This is necessary for parent to deselect and select the tool
        # in the tools menu.
        self.Bind = self.Selector.Bind


    def GetCurvedict(self, e=None):
        curvedict = dict()
        N = self.parent.notebook.GetPageCount()
        for i in np.arange(N):
            Page = self.parent.notebook.GetPage(i)
            key = Page.counter
            curve = Page.dataexp
            if curve is not None:
                curvedict[key] = curve
        return curvedict

        
    def OnClose(self, event=None):
        # This is a necessary function for PyCorrFit.
        # Do not change it.
        self.parent.toolmenu.Check(self.MyID, False)
        self.parent.ToolsOpen.__delitem__(self.MyID)
        self.Selector.Destroy()


    def OnPageChanged(self, page):
        # When parent changes
        # This is a necessary function for PyCorrFit.
        # This is stuff that should be done when the active page
        # of the notebook changes.
        self.OnClose()


    def OnResults(self, keys):
        """ Here we will close (or disable?) pages that are not wanted
            by the user. It is important that we do not close pages that
            do not contain any experimental data (Page.dataeyp is None),
            because we ignored those pages during import.
        """
        N = self.parent.notebook.GetPageCount()
        for i in np.arange(N):
            Page = self.parent.notebook.GetPage(i)
            key = Page.counter
            if keys.count(key) == 0 and Page.dataexp is not None:
                self.parent.notebook.DeletePage(i)


class UserSelectCurves(wx.Frame):
    # This tool is derived from a wx.frame.
    def __init__(self, parent, curvedict, wrapper=None):
        """
        *curvedict* is a dictionary that contains the curves. Keys serve as
        identifiers in the curve selection.
        e.g.
        curvelist["#1:"] = np.array[ np.array[0.0,1], np.array[0.0,.971] ...]
        *parent* is the main frame
        *wrapper* is the object to which the chosen keys are given back. If
        it is not None, it must provide a function *OnResults*, accepting a list
        of keys as an argument.
        """
        # parent is the main frame of PyCorrFit
        self.parent = parent
        self.wrapper = wrapper
        self.curvedict = curvedict
        # Get the window positioning correctly
        pos = self.parent.GetPosition()
        pos = (pos[0]+100, pos[1]+100)
        wx.Frame.__init__(self, parent=self.parent, title="Curve selection",
                 pos=pos, style=wx.DEFAULT_FRAME_STYLE|wx.FRAME_FLOAT_ON_PARENT)
        ## Pre-process
        self.ProcessDict()
        ## Content
        # Panel
        self.sp = wx.SplitterWindow(self, size=size, style=wx.SP_3DSASH)
        self.sp.SetMinimumPaneSize(1)
        sizepanelx = 150
        self.panel = wx.Panel(self.sp, size=(sizepanelx,300))
        self.topSizer = wx.BoxSizer(wx.VERTICAL)
        # Box selection
        # Plotting area
        # Button OK
        btnok = wx.Button(self.panel, wx.ID_ANY, 'Apply')
        self.Bind(wx.EVT_BUTTON, self.OnPushResults, btnok)
        self.topSizer.Add(btnok)
        # Finish off sizers
        self.panel.SetSizer(self.topSizer)
        self.topSizer.Fit(self)
        self.SetMinSize(self.topSizer.GetMinSizeTuple())
        # Canvas
        self.canvas = plot.PlotCanvas(self.sp)
        self.canvascorr.setLogScale((True, False))  
        self.canvascorr.SetEnableZoom(True)

        # Splitter window
        self.sp.SplitVertically(self.panel, self.canvas, sizepanelx)
        # Icon
        if parent.MainIcon is not None:
            wx.Frame.SetIcon(self, parent.MainIcon)
        self.Show(True)


        def ProcessDict(self, e=None):
            # Define the order of keys used
            self.curvekeys = self.curvedict.keys()
            self.curvekeys.sort()

        
        def OnPushResults(self, e=None):
            # Get keys from selection
            self.wrapper.OnResults(self.curvekeys)


        def OnUpdatePlot(self, e=None):
            # Get selected curves
            # Set color map
            # Clear Plot
            # Draw Plot
            pass



def Wrapper_OnImport(curvelist):
    pass
