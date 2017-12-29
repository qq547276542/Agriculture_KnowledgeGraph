function showmessage(){
	$.gritter.add({
		title: 'You Have Message!',
		text: 'You have some mesages from Anyone this time. To read any mesage <a href="#" style="color:#ccc">adn write some </a> letter, Send and Reaply.',
		image: 'img/user2.png',
		sticky: false,
		time: ''
	});
}
$(function () {

    setTimeout(showmessage,2000);
    $( "#inline-datepicker" ).datepicker();
    /* Bar Chart starts */

    var d1 = [];
    for (var i = 0; i <= 20; i += 1)
        d1.push([i, parseInt(Math.random() * 30)]);

    var d2 = [];
    for (var i = 0; i <= 20; i += 1)
        d2.push([i, parseInt(Math.random() * 30)]);


    var stack = 0, bars = true, lines = false, steps = false;
    
    function plotWithOptions() {
        $.plot($("#bar-chart"), [ d1, d2 ], {
            series: {
                stack: stack,
                lines: { show: lines, fill: true, steps: steps },
                bars: { show: bars, barWidth: 0.8 }
            },
            grid: {
                borderWidth: 0, hoverable: true, color: "#777"
            },
            colors: ["#7a4a39", "#7a4a39"],
            bars: {
                  show: true,
                  lineWidth: 0,
                  fill: true,
                  fillColor: { colors: [ { opacity: 0.9 }, { opacity: 0.8 } ] }
            }
        });
    }

    plotWithOptions();
    
    $(".stackControls input").click(function (e) {
        e.preventDefault();
        stack = $(this).val() == "With stacking" ? true : null;
        plotWithOptions();
    });
    $(".graphControls input").click(function (e) {
        e.preventDefault();
        bars = $(this).val().indexOf("Bars") != -1;
        lines = $(this).val().indexOf("Lines") != -1;
        steps = $(this).val().indexOf("steps") != -1;
        plotWithOptions();
    });

    /* Bar chart ends */

});

/* Curve chart starts */

$(function () {
    var sin = [], cos = [];
    for (var i = 0; i < 14; i += 0.5) {
        sin.push([i, Math.sin(i)]);
        cos.push([i, Math.cos(i)]);
    }

    // First Chart
    var chart1 = function(){
      $("#chart1").html("");
      var tax_data = [
         {"period": "2011 Q3", "licensed": 4369, "sorned": 3707},
         {"period": "2011 Q2", "licensed": 4756, "sorned": 3951},
         {"period": "2011 Q1", "licensed": 2146, "sorned": 1769},
         {"period": "2010 Q4", "licensed": 3746, "sorned": 3257},
         {"period": "2009 Q4", "licensed": 2185, "sorned": 1185},
         {"period": "2008 Q4", "licensed": 3155, "sorned": 2972},
         {"period": "2007 Q4", "licensed": 1813, "sorned": 1253},
         {"period": "2006 Q4", "licensed": 2974, "sorned": 2562},
         {"period": "2005 Q4", "licensed": 1235, "sorned": 150}
      ];
      
      Morris.Line({
        element: 'chart1',
        data: tax_data,
        xkey: 'period',
        hideHover: 'auto',
        ykeys: ['licensed', 'sorned'],
        labels: ['Licensed', 'Off the road']
      });
    }
    // Init First Chart
    chart1();
    // Resize First Chart on page resize
    $(window).resize(debounce(chart1,200));
    
    // Second Chart
    var graph2 = function(){
      $("#graph2").html("");
      Morris.Donut({
        element: 'graph2',
        data: [
          {label: "Internet Explorer", value: 12},
          {label: "Google Chrome", value: 30},
          {label: "Mozilla Firefox", value: 20},
          {label: "Other", value: 17}
        ],
        hideHover: 'auto',
        colors: ["#C5CED6", "#59646E","#384B5E", "#999"]
        //colors: ["#4BB5C1", "#96CA2D", "#7FC6BC","#EDF7F2"]
      });
    }
    // Init Second Chart
    graph2();
    // Resize Second Chart on page resize
    $(window).resize(debounce(graph2,200));
    
    // Third Chart
    var chart1 = function(){
      $("#bar-chart2").html("");
      Morris.Bar({
        element: 'bar-chart2',
        data: [
          { y: '2006', a: 100, b: 90 },
          { y: '2007', a: 75,  b: 65 },
          { y: '2008', a: 50,  b: 40 },
          { y: '2009', a: 75,  b: 65 },
          { y: '2010', a: 50,  b: 40 },
          { y: '2011', a: 75,  b: 65 },
          { y: '2012', a: 100, b: 90 }
        ],
        xkey: 'y',
        ykeys: ['a', 'b'],
        hideHover: 'auto',
        labels: ['Series A', 'Series B'],
        barColors: [ "#56626B","#486b60", "#999"]
      });
    
    }
    // Init Third Chart
    chart1();
    // Resize Third Chart on page resize
    $(window).resize(debounce(chart1,200));
    
    $("#pie-chart4").sparkline([55, 100, 120, 110], {
      type: 'pie',
      height: 300,
      sliceColors: ['#c5ced6','#486b60','#59646e','#C0CA55','#384b5e','#999999']
    });
    
    $("#pie-chart5").sparkline([55, 100, 44, 13], {
      type: 'pie',
      height: 70,
      sliceColors: ['#59646e','#999999','#c5ced6','#C0CA55','#384b5e','#486b60']
    });
    
    $("#pie-chart6").sparkline([55, 100, 120, 110], {
      type: 'pie',
      height: 70,
      sliceColors: ['#c5ced6','#486b60','#59646e','#C0CA55','#384b5e','#999999']
    });
    
    $('#reportrange').daterangepicker({
        startDate: moment().subtract('days', 29),
        endDate: moment(),
        minDate: '01/01/2012',
        maxDate: '12/31/2014',
        dateLimit: { days: 60 },
        showDropdowns: true,
        showWeekNumbers: true,
        timePicker: false,
        timePickerIncrement: 1,
        timePicker12Hour: true,
        ranges: {
           'Today': [moment(), moment()],
           'Yesterday': [moment().subtract('days', 1), moment().subtract('days', 1)],
           'Last 7 Days': [moment().subtract('days', 6), moment()],
           'Last 30 Days': [moment().subtract('days', 29), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract('month', 1).startOf('month'), moment().subtract('month', 1).endOf('month')]
        },
        opens: 'left',
        buttonClasses: ['btn btn-default'],
        applyClass: 'btn-small btn-primary',
        cancelClass: 'btn-small',
        format: 'MM/DD/YYYY',
        separator: ' to ',
        locale: {
            applyLabel: 'Submit',
            fromLabel: 'From',
            toLabel: 'To',
            customRangeLabel: 'Custom Range',
            daysOfWeek: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr','Sa'],
            monthNames: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            firstDay: 1
        }
     },
     function(start, end) {
      console.log("Callback has been called!");
      $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
     });
     $('#reportrange span').html(moment().subtract('days', 29).format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY'));

    
});