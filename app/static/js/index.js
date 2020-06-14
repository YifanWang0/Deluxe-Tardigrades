var grade_count = 0;
var floor_count = 0;
var location_count = 0;

//changing buttons displayed (for rendering graphs) according to option selected
var grade_btn = document.getElementById("grade");
var floor_btn = document.getElementById("floor");
var location_btn = document.getElementById("location");
var graphSelection = document.getElementById("graph");

var displayButtons = function(){
  var value = graphSelection.value;
  if (value == "lockers-trade" || value == "lockers-registered"){
    grade_btn.style.display = "none";
    floor_btn.style.display = "inline";
    location_btn.style.display = "inline";
  } else if (value == "users-buddy") {
    grade_btn.style.display = "inline";
    floor_btn.style.display = "inline";
    location_btn.style.display = "inline";
  } else if (value == "users-registered") {
    grade_btn.style.display = "inline";
    floor_btn.style.display = "none";
    location_btn.style.display = "none";
  }
}

graphSelection.addEventListener("change", function(){
  grade_count = 0;
  floor_count = 0;
  location_count = 0;
  d3.selectAll("svg").remove();
  displayButtons();
});

grade_btn.addEventListener("click", function(){
  d3.selectAll("svg").remove();
  if (graphSelection.value == "users-registered" && grade_count == 0){
    userRegistration();
  }
});

floor_btn.addEventListener("click", function(){
  d3.selectAll("svg").remove();
  if (graphSelection.value == "lockers-registered" && floor_count == 0){
    lockerRegistrationByFloor();
  }
})

location_btn.addEventListener("click", function(){
  d3.selectAll("svg").remove();
  if (graphSelection.value == "lockers-registered" && location_count == 0){
    lockerRegistrationByLocation();
  }
})

//creating donut chart for user registration data
var userRegistration = function() {
grade_count = 1;
floor_count = 0;
location_count = 0;
// set the dimensions and margins of the graph
var width = 600
    height = 600
    margin = 100

// The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
var radius = Math.min(width, height) / 2 - margin

// append the svg object to the div called 'my_dataviz'
var svg = d3.select("#svg")
.append("svg")
  .attr("width", width)
  .attr("height", height)
.append("g")
  .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

//create data
var freshman = 0;
var sophomore= 0;
var junior = 0;
var senior = 0;
for (var i=0; i < userRegistration_grade.length; i++){
  if (userRegistration_grade[i] == 9){
    freshman += 1;
  } else if (userRegistration_grade[i] == 10){
    sophomore += 1;
  } else if (userRegistration_grade[i] == 11){
    junior += 1;
  } else {
    senior += 1;
  }
}
data = {Freshman:freshman, Sophomore:sophomore, Junior:junior, Senior:senior}

// set the color scale
var color = d3.scaleOrdinal()
.domain("a", "b", "c", "d")
.range(d3.schemeDark2);

// Compute the position of each group on the pie:
var pie = d3.pie()
.sort(null) // Do not sort group by size
.value(function(d) {return d.value; })
var data_ready = pie(d3.entries(data))

// The arc generator
var arc = d3.arc()
.innerRadius(radius * 0.5)// This is the size of the donut hole
.outerRadius(radius * 0.8)

// Another arc that won't be drawn. Just for labels positioning
var outerArc = d3.arc()
.innerRadius(radius * 0.9)
.outerRadius(radius * 0.9)

// Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
svg
.selectAll('allSlices')
.data(data_ready)
.enter()
.append('path')
.attr('d', arc)
.attr('fill', function(d){ return(color(d.data.key)) })
.attr("stroke", "white")
.style("stroke-width", "2px")
.style("opacity", 0.7)

// Add the polylines between chart and labels:
svg
.selectAll('allPolylines')
.data(data_ready)
.enter()
.append('polyline')
  .attr("stroke", "black")
  .style("fill", "none")
  .attr("stroke-width", 1)
  .attr('points', function(d) {
    var posA = arc.centroid(d) // line insertion in the slice
    var posB = outerArc.centroid(d) // line break: we use the other arc generator that has been built only for that
    var posC = outerArc.centroid(d); // Label position = almost the same as posB
    var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2 // we need the angle to see if the X position will be at the extreme right or extreme left
    posC[0] = radius * 0.95 * (midangle < Math.PI ? 1 : -1); // multiply by 1 or -1 to put it on the right or on the left
    return [posA, posB, posC]
  })

// Add the polylines between chart and labels:
svg
.selectAll('allLabels')
.data(data_ready)
.enter()
.append('text')
  .text( function(d) { return d.data.key } )
  .attr('transform', function(d) {
      var pos = outerArc.centroid(d);
      var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
      pos[0] = radius * 0.99 * (midangle < Math.PI ? 1 : -1);
      return 'translate(' + pos + ')';
  })
  .style('text-anchor', function(d) {
      var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
      return (midangle < Math.PI ? 'start' : 'end')
  })
}

//creating bar graph for locker registration
var lockerRegistrationByFloor = function() {
grade_count = 0;
floor_count = 1;
location_count = 0;

var data = [];

var first = 0
    second = 0
    third = 0
    fourth = 0
    fifth = 0
    sixth = 0
    seventh = 0
    eighth = 0
    ninth = 0
    tenth = 0
for (var i=0; i<lockerRegistration_floor.length; i++){
  if (lockerRegistration_floor[i] == 1){
    first += 1;
  } else if (lockerRegistration_floor[i] == 2){
    second += 1;
  } else if (lockerRegistration_floor[i] == 3){
    third += 1;
  } else if (lockerRegistration_floor[i] == 4){
    fourth += 1;
  } else if (lockerRegistration_floor[i] == 5){
    fifth += 1;
  } else if (lockerRegistration_floor[i] == 6){
    sixth += 1;
  } else if (lockerRegistration_floor[i] == 7){
    seventh += 1;
  } else if (lockerRegistration_floor[i] == 8){
    eighth += 1;
  } else if (lockerRegistration_floor[i] == 9){
    ninth += 1;
  } else {
    tenth += 1;
  }
}

var data =  [{"floor":1, "number":first},
             {"floor":2, "number":second},
             {"floor":3, "number":third},
             {"floor":4, "number":fourth},
             {"floor":5, "number":fifth},
             {"floor":6, "number":sixth},
             {"floor":7, "number":seventh},
             {"floor":8, "number":eighth},
             {"floor":9, "number":ninth},
             {"floor":10, "number":tenth},]

//defining the margin amounts of the chart
var margin = {top:50, right:50, bottom:50, left:50};
//the total width of the bar graph
var height = 3*200-100;
//the total height of the bar graph
var width = 800-100;


//sets the number of pixels for the yscale
//adds padding
var yScale = d3.scaleBand()
    .range([0, height])
    .paddingInner(0.08)

//sets the number of pixels for the xscale
var xScale = d3.scaleLinear()
    .range([0,width-50]);

//positions the x axis on the top
var xAxis = d3.axisTop(xScale)
//positions the y axis on the left
var yAxis = d3.axisLeft(yScale);


//makes a chart with width and height adjusted with margins
var svgContainer = d3.select("#svg").append("svg")
    .attr("width", width+100)
    .attr("height",height+100)
    .append("g").attr("class", "container")
    .attr("transform", "translate("+ 50 +","+ 50 +")");

    yScale.domain(data.map(function(d) { return d.floor; }));
      yAxis = d3.axisLeft(yScale);

      xScale.domain([0, d3.max(data, function(d) { return d.number+2; })]);
      xAxis = d3.axisTop(xScale);

      //draws the actual bars and does the height based off of data values
      bars = svgContainer.selectAll(".bar")
          .data(data)
          .enter()
          .append("g")

      bars.append("rect")
          .attr("class", "bar")
          .attr("y", function(d) { return yScale(d.floor); })
          .attr("height", yScale.bandwidth())
          .attr("x", function(d) { return 0; })
          .attr("width", function(d) { return xScale(d.number); })
          .style("fill", "#f6d8b9");

      //make the numbers on the labels, x value and y value of the numerical labels
      labeling = svgContainer.selectAll(".text")
          .data(data)
          .enter()

      labeling.append("text")
          .attr("class","label")
          .attr("y", (function(d) { return yScale(d.floor)  + (yScale.bandwidth())/2 + 6 ; }  ))
          .attr("x", function(d) { return  xScale(d.number) + 10; })
          .attr("dx", ".25em")
          .text(function(d) { return d.number; });


      //creates labels for y scale on the side
      svgContainer.append("g")
          .attr("class", "xaxis")
          .call(xAxis)
          .selectAll("text")
          // .attr("font-family", "Didot")

      svgContainer.append("g")
          .attr("class", "yaxis")
          .call(yAxis)
          .selectAll("text")
          // .attr("font-family", "Didot")

      svgContainer.append("text")
          .attr("transform",
                "translate(" + (width/2) + " ," +
                               (margin.top - 85) + ")")
          .style("text-anchor", "middle")
          .text("Number of Lockers Registered");

      svgContainer.append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 0 - margin.left)
          .attr("x",0 - (height / 2))
          .attr("dy", "1em")
          .style("text-anchor", "middle")
          .text("Floor");
}

var lockerRegistrationByLocation = function() {
grade_count = 0;
floor_count = 0;
location_count = 1;

var parsedList = []
var quoteCount = 0
var word= '';
for (var i=0; i<lockerRegistration_location.length; i++){
  if (lockerRegistration_location[i] == "'"){
    quoteCount += 1;
  } else{
    if (quoteCount%2 != 0){
      word = word + lockerRegistration_location[i];
    } else if (quoteCount%2 == 0 && quoteCount != 0 && lockerRegistration_location[i] != ' '){
      parsedList.push(word);
      word = '';
    }
  }
};

var data = [];

var hallway = 0
    bar = 0
    robotics = 0
    music_hallway = 0
    atrium = 0
    swim_gym = 0
    gym = 0

for (var i=0; i<parsedList.length; i++){
  if (parsedList[i] == "Hallway"){
    hallway += 1;
  } else if (parsedList[i] == "Bar") {
    bar += 1;
  } else if (parsedList[i] == "Robotics") {
    robotics += 1;
  } else if (parsedList[i] == "Music Hallway") {
    music_hallway += 1;
  } else if (parsedList[i] == "Atrium") {
    atrium += 1;
  } else if (parsedList[i] == "Swim Gym") {
    swim_gym += 1;
  } else if (parsedList[i] == "Gym") {
    gym += 1;
  }
}

data = [{"location": "Hallway", "number": hallway},
        {"location": "Bar", "number": bar},
        {"location": "Robotics", "number": robotics},
        {"location": "Music Hallway", "number": music_hallway},
        {"location": "Atrium", "number": atrium},
        {"location": "Swim Gym", "number": swim_gym},
        {"location": "Gym", "number": gym}]

//defining the margin amounts of the chart
var margin = {top:50, right:50, bottom:50, left:50};
//the total width of the bar graph
var height = 3*200-100;
//the total height of the bar graph
var width = 800-100;


//sets the number of pixels for the yscale
//adds padding
var yScale = d3.scaleBand()
    .range([0, height])
    .paddingInner(0.08)

//sets the number of pixels for the xscale
var xScale = d3.scaleLinear()
    .range([0,width-50]);

//positions the x axis on the top
var xAxis = d3.axisTop(xScale)
//positions the y axis on the left
var yAxis = d3.axisLeft(yScale);


//makes a chart with width and height adjusted with margins
var svgContainer = d3.select("#svg").append("svg")
    .attr("width", width+100)
    .attr("height",height+100)
    .append("g").attr("class", "container")
    .attr("transform", "translate("+ 100 +","+ 50 +")");

    yScale.domain(data.map(function(d) { return d.location; }));
      yAxis = d3.axisLeft(yScale);

      xScale.domain([0, d3.max(data, function(d) { return d.number+2; })]);
      xAxis = d3.axisTop(xScale);

      //draws the actual bars and does the height based off of data values
      bars = svgContainer.selectAll(".bar")
          .data(data)
          .enter()
          .append("g")

      bars.append("rect")
          .attr("class", "bar")
          .attr("y", function(d) { return yScale(d.location); })
          .attr("height", yScale.bandwidth())
          .attr("x", function(d) { return 0; })
          .attr("width", function(d) { return xScale(d.number); })
          .style("fill", "#f6d8b9");

      //make the numbers on the labels, x value and y value of the numerical labels
      labeling = svgContainer.selectAll(".text")
          .data(data)
          .enter()

      labeling.append("text")
          .attr("class","label")
          .attr("y", (function(d) { return yScale(d.location)  + (yScale.bandwidth())/2 + 6 ; }  ))
          .attr("x", function(d) { return  xScale(d.number) + 10; })
          .attr("dx", ".25em")
          .text(function(d) { return d.number; });


      //creates labels for y scale on the side
      svgContainer.append("g")
          .attr("class", "xaxis")
          .call(xAxis)
          .selectAll("text")
          // .attr("font-family", "Didot")

      svgContainer.append("g")
          .attr("class", "yaxis")
          .call(yAxis)
          .selectAll("text")
          // .attr("font-family", "Didot")

      svgContainer.append("text")
          .attr("transform",
                "translate(" + (width/2) + " ," +
                               (margin.top - 85) + ")")
          .style("text-anchor", "middle")
          .text("Number of Lockers Registered");

      svgContainer.append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 0 - margin.left - 49)
          .attr("x",0 - (height / 2))
          .attr("dy", "1em")
          .style("text-anchor", "middle")
          .text("Location");
}
