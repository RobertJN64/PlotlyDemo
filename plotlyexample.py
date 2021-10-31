import plotly.express as px
#import json

gapminderdf = px.data.gapminder(pretty_names=True)

x = 'GDP per Capita'
y = 'Life Expectancy'
color = 'Continent'
animaxis = 'Year'
size = 'Population'
name = 'Country'

rangex = [gapminderdf[x].min() * 0.9, gapminderdf[x].max() * 1.1]
rangey = [gapminderdf[y].min() * 0.9, gapminderdf[y].max() * 1.1]

fig = px.scatter(gapminderdf, x=x, y=y, animation_frame=animaxis, size=size, color=color, log_x=True,
                 hover_name=name, size_max=55, range_x=rangex, range_y=rangey)

# Exports
# with open('FigSaves/demopage.html', 'w+') as f:
#     f.write(fig.to_html())
#
# with open('FigSaves/demopage.json', 'w+') as f:
#     j = json.loads(fig.to_json())
#     json.dump(j, f, indent=2)
#
# with open('FigSaves/demopageimg.png', 'wb+') as f:
#     f.write(fig.to_image())
fig.show()