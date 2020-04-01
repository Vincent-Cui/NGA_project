#!/usr/bin/env python
# coding: utf-8

# In[1]:


import geopandas as gpd
import json
#from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer
from bokeh.io import curdoc
from bokeh.models import Slider, HoverTool
from bokeh.layouts import widgetbox, row, column

# In[101]:


shapefile = 'dataset/LGA_NGA.json'
gdf = gpd.read_file(shapefile)


# In[21]:


#pd.options.display.max_columns = 100
#pd.options.display.max_rows = 999


# In[103]:


import pandas as pd
datafile = 'dataset/MGWR_results.csv'
df = pd.read_csv(datafile)
filter = df['p_ndifgdp'].between(0,0.1)
df1 = df[filter]


# In[105]:



#Define function that returns json_data for year selected by user.
    
def json_data(selectedYear):
    yr = selectedYear
    df_yr = df1[df1['yr'] == yr]
    merged = gdf.merge(df_yr, left_index=True, right_on = 'LGA', how = 'left')
    merged.fillna({'beta_ndifgdp': 'No data'}, inplace = True)
    merged_json = json.loads(merged.to_json())
    json_data = json.dumps(merged_json)
    return json_data
#Input GeoJSON source that contains features for plotting.
geosource = GeoJSONDataSource(geojson = json_data(2001))
#Define a sequential multi-hue color palette.
palette = brewer['YlGnBu'][8]
#Reverse color order so that dark blue is highest coefficient.
palette = palette[::-1]
#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 10, nan_color = '#d9d9d9')
#Add hover tool
hover = HoverTool(tooltips = [ ('LGA ID','@LGA'),('GDP Coef', '@beta_ndifgdp'),('POP Coef', '@beta_ndifpop'), ('Access Coef', '@beta_MEAN_Access') ])
#Create color bar. 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal')
#Create figure object.
p = figure(title = 'GDP coef, 2001', plot_height = 600 , plot_width = 600, toolbar_location = None, tools = [hover])
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
#Add patch renderer to figure. 
p.patches('xs','ys', source = geosource,fill_color = {'field' :'beta_ndifgdp', 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)
#Specify layout
p.add_layout(color_bar, 'below')
# Define the callback function: update_plot
def update_plot(attr, old, new):
    yr = slider.value
    new_data = json_data(yr)
    geosource.geojson = new_data
    p.title.text = 'GDP coef, %d' %yr
    
# Make a slider object: slider 
slider = Slider(title = 'Year',start = 2001, end = 2015, step = 1, value = 2001)
slider.on_change('value', update_plot)
# Make a column layout of widgetbox(slider) and plot, and add it to the current document
layout = column(p,widgetbox(slider))
curdoc().add_root(layout)
#Display plot inline in Jupyter notebook
#output_notebook()
#Display plot
#show(layout)


# In[ ]:




