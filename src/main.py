import wx
from application_input import ApplicationInputFrame
from assigner import AssignerFrame
from checkin import CheckinFrame


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Camp Registration System", size=(600, 400))

        notebook = wx.Notebook(self)

        self.application_input_tab = ApplicationInputFrame(notebook)
        notebook.AddPage(self.application_input_tab, "Application Input")

        self.assigner_tab = AssignerFrame(notebook)
        notebook.AddPage(self.assigner_tab, "Assigner")

        self.checkin_tab = CheckinFrame(notebook)
        notebook.AddPage(self.checkin_tab, "Check-in")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Show()


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()