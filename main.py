import TKinterModernThemes as TKMT
import plotly.express as px
import tkinter as tk
import pandas
import copy

#TODO - dif data sets
#TODO - dif plot styles

class Param:
    def __init__(self, displayname, kwargname, default=None, required=True):
        self.displayname = displayname
        self.kwargname = kwargname
        self.required = required
        self.var = tk.StringVar(value=default)

class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Plotly Demo Launcher")

        self.df: pandas.DataFrame = px.data.gapminder(pretty_names=True)
        configFrame = self.addLabelFrame("Configuration Options")
        options = list(self.df.columns)
        mandatoryoptions = ["Choose an Option: "] + copy.copy(options)
        optionaloptions = ["(Optional)"] + copy.copy(options)

        self.params = [Param("X Axis", "x", "GDP per Capita"),
                       Param("Y Axis", "y", "Life Expectancy"),
                       Param("Name", "hover_name", "Country", False),
                       Param("Color", "color", "Continent", False),
                       Param("Size", "size", "Population", False),
                       Param("Anim Axis", "animation_frame", "Year", False)]


        for param in self.params:
            configFrame.Text(param.displayname)
            options = mandatoryoptions if param.required else optionaloptions
            configFrame.OptionMenu(options, param.var, default=param.var.get())

        self.nextCol()
        settingsFrame = self.addLabelFrame("Graph Settings")

        self.logxvar = tk.BooleanVar(value=True)
        self.logyvar = tk.BooleanVar()
        self.size_max = tk.IntVar(value=50)
        settingsFrame.SlideSwitch("Log X", self.logxvar)
        settingsFrame.SlideSwitch("Log Y", self.logyvar)
        settingsFrame.Text("Max Point Size: ")
        settingsFrame.NumericalSpinbox(0, 100, 5, self.size_max)

        settingsFrame.Blank()
        settingsFrame.Seperator()
        settingsFrame.Blank()

        settingsFrame.AccentButton("Create Graph", self.createGraph)

        self.run()

    def createGraph(self):
        kwargs = {"log_x": self.logxvar.get(), "log_y": self.logyvar.get(), "size_max": self.size_max.get()}
        for param in self.params:
            value = param.var.get()
            if value == "Choose an Option: ":
                return
            if value != "(Optional)":
                kwargs[param.kwargname] = value

        rangex = [self.df[kwargs['x']].min() * 0.9, self.df[kwargs['x']].max() * 1.1]
        rangey = [self.df[kwargs['y']].min() * 0.9, self.df[kwargs['y']].max() * 1.1]
        kwargs['range_x'] = rangex
        kwargs['range_y'] = rangey

        fig = px.scatter(self.df, **kwargs)
        fig.show()
        #import plotlylocalviewer
        #plotlylocalviewer.save(fig)
        #plotlylocalviewer.view()

if __name__ == '__main__':
    App()