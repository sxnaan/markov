d3.json("https://raw.githubusercontent.com/sxnaan/markov/main/src/data.json", function(data) {

    var w = 1400;
    var h = 800;
    var linkDistance = 100;

    var colors = d3.scale.category10();

    var svg = d3.select("body").append("svg").attr({"width":w,"height":h});

    var force = d3.layout.force()
        .nodes(data.nodes)
        .links(data.links)
        .size([w,h])
        .linkDistance([linkDistance])
        .charge([-500])
        .theta(0.1)
        .gravity(0.05)
        .start();

    var nodes = svg.selectAll("circle")
        .data(data.nodes)
        .enter()
        .append("circle")
        .attr({"r":15})
        .style("fill",function(d,i){return colors(i);})
        .call(force.drag)

    var nodelabels = svg.selectAll(".nodelabel") 
        .data(data.nodes)
        .enter()
        .append("text")
        .attr({"x":function(d){return d.x;},
               "y":function(d){return d.y;},
               "class":"nodelabel",
               "stroke":"black"})
        .text(function(d){return d.id;});

    var edgepaths = svg.selectAll(".edgepath")
        .data(data.edges)
        .enter()
        .append('path')
        .attr({'d': function(d) {return 'M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y},
               'class':'edgepath',
               'fill-opacity':0,
               'stroke-opacity':0,
               'fill':'blue',
               'stroke':'red',
               'strok-width':function(d) {return d.links.weight * 10},
               'id':function(d,i) {return 'edgepath'+i}})
        .style("pointer-events", "none");

    svg.append('defs').append('marker')
        .attr({'id':'arrowhead',
               'viewBox':'-0 -5 10 10',
               'refX':25,
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
                                          return path});       

    });

});