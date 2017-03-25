#Gap Minder Clone

This project is an attempt to mimic the features of the well known [Gap-Minder](http://www.gapminder.org/) interactive [chart](https://www.gapminder.org/world/#$majorMode=chart$is;shi=t;ly=2003;lb=f;il=t;fs=11;al=30;stl=t;st=t;nsl=t;se=t$wst;tts=C$ts;sp=5.59290322580644;ti=2011$zpv;v=0$inc_x;mmid=XCOORDS;iid=phAwcNAVuyj1jiMAkmq1iMg;by=ind$inc_y;mmid=YCOORDS;iid=pyj6tScZqmEfbZyl0qjbiRQ;by=ind$inc_s;uniValue=8.21;iid=phAwcNAVuyj0XOoBL_n5tAQ;by=ind$inc_c;uniValue=255;gid=CATID0;by=grp$map_x;scale=log;dataMin=194;dataMax=96846$map_y;scale=lin;dataMin=0.0095;dataMax=27$map_s;sma=50;smi=2$cd;bd=0$inds=), using the [Bokeh](http://bokeh.pydata.org/en/latest/) interactive visualization library. This started as the final project for the DataCamp course on Bokeh taught by Bryan Van de Ven. I enjoyed the class a lot but, all of the course projects were done in the browser, within an environment set up with local variables to allow students to focus on the course content. I really enjoyed this project, so I decided to revisit it by building the project from scratch locally and adding some extra features along the way.

The original project allowed users to:
* Select a value for x and y axes
* Select a year to display via slider
* Hover over points to see the various values assocaited with each point

Added features:
* Select a value to scale point size as well as max and min point size
* Select between linear and log scale for x, y and size
* Play, Stop, Reverse, Forward and Back buttons to move through year values
* Moved legend outside of plot area to prevent it from obscuring view of plot
* Reads data in from AWS S3 stored flat file to allow for the app to be hosted on Heroku

Features I would like to add:
* Input that allows user to set Play/Reverse speed
* Toggle visibility of Legend
* Map visual like the actual gapminder dash?



