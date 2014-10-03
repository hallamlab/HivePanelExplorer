'''
created 06/05/2014

by sperez

contains all the pieces of the html and d3 functions to plot the hive
'''

htmlDoc = """<!comment This is a hive plot developed using HivePlotter.>
<!DOCTYPE html>
<meta charset="utf-8">
<body>
<script src="http://d3js.org/d3.v3.min.js"></script>
<script src="http://d3js.org/d3.hive.v0.min.js"></script>
<div id="container" style="width:{16}px">
<div id="title" style="height:70px;width:550px;float:left;"></div>
<div id="rules" style="height:200px;width:450px;float:right;border-bottom:2px solid #5C5C5C"></div>
<div id="hive" style="height:{17}px;width:{17}px;float:left;"></div>
<div id="reveal" style="height:60px;width:450px;float:left;"></div></div>

<script src="{0}"></script>
<script src="{1}"></script>
<script>
//All the user defined parameters

var SVGTitle = 'Hive plot : ' + '{2}'

var colorNeutral = '{3}'

var num_axis = {4}

var angle = {5}

var nodeColor = '{6}'
    edgeColor = {7}
    linkwidth = {13}
    oplink = {14}
    opnode = {15}

var revealNode = function(d,color){{
    d3.select("body").select("#reveal").append("p")
        .html({8})
        .style("color", color)
    }};
var revealLink = function(d,color){{
    d3.select("body").select("#reveal").append("p")
        .html({9})
        .style("color", color)
    }};

d3.select("body").select("#rules")
    .append("p")
    .html('<br><br>Node assignment property: ' + '{10}' + '<br><br>Node positioning property: ' + '{11}' + '<br><br>Edge coloring property: ' + '{12}') 
    .style("color", colorNeutral)

d3.select("body").select("#title")
    .append("h2").html('<center>'+SVGTitle+'</center>')
    .style("color", colorNeutral)
    
var removeReveal = function(d){{
    d3.select("body").select("#reveal").selectAll("p")
        .transition()
        .duration(hoverOverTime)
        .style("opacity", 0)
        .remove();
    }};
    
var nodesize = 4
    nodestroke = 0.4
    nodestrokecolor = "grey"
    
var width = document.getElementById("hive").offsetWidth
    height = document.getElementById("hive").offsetHeight
    innerRadius = 40,
    outerRadius = width*0.4;

var linkfill = "none"
    bkgcolor = "white"

var hoverOverTime = 900

var radius = d3.scale.linear().range([innerRadius, outerRadius]);

var angles = d3.scale.ordinal()
    .domain(d3.range(num_axis))
    .range(angle);

var link_color = d3.scale.linear()
    .domain(d3.range(0,edgeColor.length,1.0))
    .range(edgeColor);

var svg = d3.select("body").select("#container").select("#hive").append("svg")
    .attr("class", SVGTitle)
    .attr("width", width)
    .attr("height", height)
    .style("background-color", bkgcolor)
  .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
    
svg.selectAll(".axis")
    .data(angle)
  .enter().append("line")
    .attr("class", "axis")
    .attr("transform", function(d) {{ return "rotate(" + degrees(angles(d)) + ")"; }})
    .attr("x1", radius.range()[0])
    .attr("x2", radius.range()[1])
    .attr("stroke-width",0.7)
    .attr("stroke", "black");

svg.selectAll(".link")
    .data(links)
  .enter().append("path")
    .attr("class", "link")
    .attr("d", d3.hive.link()
    .angle(function(d) {{ return angles(d.axis); }})
    .radius(function(d) {{ return radius(d.pos); }}))
    .style("fill", linkfill)
    .style("stroke-opacity", oplink)
    .style("stroke", function(d) {{
        if (edgeColor.length == 1){{
            return edgeColor}}
        else {{return link_color(d.type)}}
        }})
    .style("stroke-width", linkwidth)
    .on("mouseover", function(d){{
            revealLink(d, d3.select(this).style("stroke"));
            d3.select(this)
                .style("stroke-opacity", 1)
                .style("stroke-width", linkwidth*2)}})
    .on("mouseout", function(d){{
            removeReveal();
            d3.select(this)
                .transition()
                .duration(800)
                .style("stroke-opacity", oplink)
                .style("stroke-width", linkwidth)}});
  
svg.selectAll(".node")
    .data(nodes)
  .enter().append("circle")
    .attr("class", "node")
    .attr("transform", function(d) {{ return "rotate(" + degrees(angles(d.axis)) + ")"; }})
    .attr("cx", function(d) {{ return radius(d.pos); }})
    .attr("r", nodesize)
    .attr("stroke-width", nodestroke)
    .attr("stroke", nodestrokecolor)
    .style("fill-opacity", opnode)
    .style("fill", nodeColor)
    .on("mouseover", function(d){{
            d3.select(this)
                .style("fill-opacity", 1)
                .attr("stroke-width", nodestroke*3)
                .attr("stroke", 'black')
                .attr("r", nodesize*1.5) 
               revealNode(d, d3.select(this).style("fill"));
            d3.selectAll(".node")
                .transition()
                .duration(hoverOverTime*0.2)
                .style("fill-opacity", function(n){{
                    if (n.name == d.name){{
                        return 1}}
                    else {{
                        return opnode}}
                }})
                .style("stroke-width", function(n){{
                    if (n.name == d.name){{
                        return nodestroke*3}}
                    else {{
                        return nodestroke}}
                }})
                .attr("stroke", function(n){{
                    if (n.name == d.name){{
                        return 'black'}}
                    else {{
                        return nodestrokecolor}}
                }})
                .attr("r", function(n){{
                    if (n.name == d.name){{
                        return nodesize*1.5}}
                    else {{
                        return nodesize}}
                }})
            d3.selectAll(".link")
                .transition()
                .delay(hoverOverTime*0.1)
                .duration(hoverOverTime*0.2)
                .style("stroke-opacity", function(l){{
                    if (l.source.name == d.name || l.target.name == d.name){{
                        return 1}}
                    else {{
                        return oplink}}
                }})
                .style("stroke-width", function(l){{
                    if (l.source.name == d.name || l.target.name == d.name){{
                        return linkwidth*2.5}}
                    else {{
                        return linkwidth}}
                }})
            }})
    .on("mouseout", function(d){{
            d3.select(this)
                .transition()
                .duration(hoverOverTime)
                .style("fill-opacity", opnode)
                .attr("stroke-width", nodestroke)
                .attr("stroke", nodestrokecolor)
                .attr("r", nodesize);
            removeReveal();
            d3.selectAll(".link")
                .transition()
                .duration(hoverOverTime)
                .style("stroke-opacity", oplink)
                .style("stroke-width", linkwidth)
            d3.selectAll(".node")
                .transition()
                .duration(hoverOverTime)
                .attr("r", nodesize)
                .attr("stroke-width", nodestroke)
                .attr("stroke", nodestrokecolor)
                .style("fill-opacity", opnode)
            }});

function degrees(radians) {{
  return radians / Math.PI * 180 - 90;
}}
</script>
</body>
</html>
"""

#more to be added
