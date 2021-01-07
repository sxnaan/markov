import "https://raw.githubusercontent.com/sxnaan/d3/main/d3.min.js";

// 16:9
const w = 1024;
const h = 576;
  
const linkDistance=50;

var colors = d3.scale.category20();

// use the public github file instead of local file to get around Chrome blocking CORS/XMLHttp (without an extension)
d3.json("https://raw.githubusercontent.com/sxnaan/markov/main/src/data.json", function (dataset) {
    var svg = d3.select("#container").append("svg").attr({"width":w,"height":h});

    var force = d3.layout.force()
    .nodes(dataset.nodes)
    .links(dataset.edges)
    .size([w,h])
    .linkDistance([linkDistance])
    .charge([-500])
    .theta(0.1)
    .gravity(0.1)
    .start();

    var edges = svg.selectAll("line")
    .data(dataset.edges)
    .enter()
    .append("line")
    .attr("id",function(d,i) {return 'edge'+i})
    .attr('marker-end','url(#arrowhead)')
    .style("stroke","#ccc")
    .style("pointer-events", "none");

    var edgepaths = svg.selectAll(".edgepath")
    .data(dataset.edges)
    .enter()
    .append('path')
    .attr({'d': function(d) {return 'M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y},
            'class':'edgepath',
            'fill-opacity':0,
            'stroke-opacity':0.4,
            'fill':'blue',
            'stroke':'grey',
            'stroke-width':function(d) {return String(d.weight*5).concat('px')},})
    .style("pointer-events", "none");

    var nodes = svg.selectAll("circle")
    .data(dataset.nodes)
    .enter()
    .append("circle")
    .attr({"r":10})
    .style("fill",function(d,i){return colors(i);})
    .call(force.drag)

    var nodelabels = svg.selectAll(".nodelabel") 
    .data(dataset.nodes)
    .enter()
    .append("text")
    .attr({"x":function(d){return d.x;},
            "y":function(d){return d.y;},
            "class":"nodelabel",
            "stroke":"black",
            "stroke-width":'.7px'})
    .text(function(d){return d.word;});

    svg.append('defs').append('marker')
        .attr({'id':'arrowhead',
            'viewBox':'-0 -5 10 10',
            'refX':20,
            'refY':0,
            //'markerUnits':'strokeWidth',
            'orient':'auto',
            'markerWidth':10,
            'markerHeight':10,
            'xoverflow':'visible'})
        .append('svg:path')
            .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
            .attr('fill', '#ccc')
            .attr('stroke','#ccc');
    

        force.on("tick", function(){

            edges.attr({"x1": function(d){return d.source.x;},
                        "y1": function(d){return d.source.y;},
                        "x2": function(d){return d.target.x;},
                        "y2": function(d){return d.target.y;}
            });

            nodes.attr({"cx":function(d){return d.x;},
                        "cy":function(d){return d.y;}
            });

            nodelabels.attr("x", function(d) { return d.x; }) 
                    .attr("y", function(d) { return d.y; });

            edgepaths.attr('d', function(d) { var path='M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y;
                                            //console.log(d)
                                            return path});        
        });

});