//changing buttons displayed (for rendering graphs) according to option selected
var grade_btn = document.getElementById("grade");
var floor_btn = document.getElementById("floor");
var location_btn = document.getElementById("location");
var graphSelection = document.getElementById("graph");

var displayButtons = function(){
  var value = graphSelection.value;
  if (value == "lockers-trade" || value == "popularity"){
    grade_btn.style.display = "none";
    floor_btn.style.display = "inline";
    location_btn.style.display = "inline";
  } else if (value == "users-buddy" || value == "lockers-registered") {
    grade_btn.style.display = "inline";
    floor_btn.style.display = "inline";
    location_btn.style.display = "inline";
  }
}

graphSelection.addEventListener("change", displayButtons);

//trying to get a graph to work
var svgWidth = 500;
var svgHeight = 300;

var svg = d3.select('svg')
  .attr("width", svgWidth)
  .attr("height", svgHeight);

var dataset = [80, 100, 56, 120, 180, 30, 40, 120, 160];

var barPadding = 5;
var barWidth = (svgWidth / dataset.length);

var barChart = svg.selectAll("rect")
  .data(dataset)
  .enter()
  .append("rect")
  .attr("y", function(d) {
    return svgHeight - d
  })
  .attr("height", function(d) {
    return d;
  })
  .attr("width", barWidth - barPadding)
  .attr("transform", function (d, i) {
    var translate = [barWidth * i, 0];
    return "translate("+ translate +")";
  });
