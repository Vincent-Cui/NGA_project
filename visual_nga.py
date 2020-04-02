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
from bokeh.layouts import gridplot
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
filter1 = df['p_ndifgdp'].between(0,0.1)
filter2 = df['p_ndifpop'].between(0,0.1)
df1 = df[filter1]
df2 = df[filter2]


# In[105]:



#Define function that returns json_data for year selected by user.
    
def json_data(selectedYear):
    yr = selectedYear
    df1_yr = df1[df1['yr'] == yr]
    df2_yr = df2[df2['yr'] == yr]
    merged1 = gdf.merge(df1_yr, left_index=True, right_on = 'LGA', how = 'left')
    merged1.fillna({'beta_ndifgdp': 'No data'}, inplace = True)
    merged2 = gdf.merge(df2_yr, left_index=True, right_on = 'LGA', how = 'left')
    merged2.fillna({'beta_ndifpop': 'No data'}, inplace = True)
    merged_json1 = json.loads(merged1.to_json())
    json_data1 = json.dumps(merged_json1)
    merged_json2 = json.loads(merged2.to_json())
    json_data2 = json.dumps(merged_json2)
    return json_data1, json_data2
#Input GeoJSON source that contains features for plotting.
json1, json2 = json_data(2001)
geosource1  = GeoJSONDataSource(geojson = json1)
geosource2  = GeoJSONDataSource(geojson = json2)
#Define a sequential multi-hue color palette.
palette = brewer['YlGnBu'][8]
#Reverse color order so that dark blue is highest coefficient.
palette = palette[::-1]
#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
color_mapper1 = LinearColorMapper(palette = palette, low = 0, high = 10, nan_color = '#d9d9d9')
color_mapper2 = LinearColorMapper(palette = palette, low = -0.3, high = 0.5, nan_color = '#d9d9d9')
#Add hover tool
hover = HoverTool(tooltips = [ ('LGA ID','@LGA'), ('Local R2','@localR2'), ('GDP Coef', '@beta_ndifgdp'),('POP Coef', '@beta_ndifpop'), ('Access Coef', '@beta_MEAN_Access') ])
#Create color bar. 
color_bar1 = ColorBar(color_mapper=color_mapper1, label_standoff=8,width = 500, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal')
color_bar2 = ColorBar(color_mapper=color_mapper2, label_standoff=8,width = 500, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal')
#Create figure object.
p1 = figure(title = 'GDP coef, 2001', plot_height = 600 , plot_width = 600, toolbar_location = None, tools = [hover])
p2 = figure(title = 'POP coef, 2001', plot_height = 600 , plot_width = 600, toolbar_location = None, tools = [hover])
p1.xgrid.grid_line_color = None
p1.ygrid.grid_line_color = None
p2.xgrid.grid_line_color = None
p2.ygrid.grid_line_color = None
#Add patch renderer to figure. 
p1.patches('xs','ys', source = geosource1,fill_color = {'field' :'beta_ndifgdp', 'transform' : color_mapper1},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)
p2.patches('xs','ys', source = geosource2,fill_color = {'field' :'beta_ndifpop', 'transform' : color_mapper2},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)
#Specify layout
p1.add_layout(color_bar1, 'below')
p2.add_layout(color_bar2, 'below')
# Define the callback function: update_plot
def update_plot(attr, old, new):
    yr = slider.value
    new_data1, new_data2 = json_data(yr)
    geosource1.geojson = new_data1
    geosource2.geojson = new_data2
    p1.title.text = 'GDP coef, %d' %yr
    p2.title.text = 'POP coef, %d' %yr
    
# Make a slider object: slider 
slider = Slider(title = 'Year',start = 2001, end = 2015, step = 1, value = 2001)
slider.on_change('value', update_plot)
# Make a column layout of widgetbox(slider) and plot, and add it to the current document
layout = gridplot([[p1, p2], [widgetbox(slider), None]])
curdoc().add_root(layout)
#Display plot inline in Jupyter notebook
#output_notebook()
#Display plot
#show(layout)


# In[ ]:




