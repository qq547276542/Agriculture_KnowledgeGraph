var Script = function () {

    $(".sparkline").each(function(){
        var $data = $(this).data();

        $data.valueSpots = {'0:': $data.spotColor};

        $(this).sparkline( $data.data || "html", $data,
        {
            tooltipFormat: '<span style="display:block; padding:0px 10px 12px 0px;">' +
            '<span style="color: {{color}}">&#9679;</span> {{offset:names}} ({{percent.1}}%)</span>'
        });
    });

    /* sparkline chart  */
    // barchart
    $("#barchart").sparkline([9,8,7,6,5,6,8,6,8,9,6,8,6,5,7,6,5,4,7,4,7,5,6,9], {
        type: 'bar',
        height: '125',
        barWidth: 8,
        barSpacing: 5,
        barColor: 'rgba(255,255,255,0.6)'
    });
    $("#barchart-2").sparkline([9,8,7,6,5,6,8,6,8,9,6,8,6,5,7,6,5,4,7,4,7,5,6,9,7,5], {
        type: 'bar',
        height: '125',
        barWidth: 30,
        barSpacing: 10,
        barColor: 'rgba(252,52,57,0.6)'
    });
    
    // linechart    
    $("#linechart").sparkline([1,5,3,7,9,3,6,4,7,9,7,6,2], {
        type: 'line',
        width: '300',
        height: '75',
        fillColor: '',
        lineColor: '#fff',
        lineWidth: 2,
        spotColor: '#fff',
        minSpotColor: '#fff',
        maxSpotColor: '#fff',
        highlightSpotColor: '#fff',
        highlightLineColor: '#ffffff',
        spotRadius: 4,
        highlightLineColor: '#ffffff'
//        tooltipFormat: '<span style="display:block; padding:0px 10px 12px 0px;">' +
//            '<span style="color: {{color}}">&#9679;</span> {{offset:names}} ({{percent.1}}%)</span>'



    });

    $("#pie-chart").sparkline([5,3,4,1,2], {
        type: 'pie',
        width: '100',
        height: '100',
        borderColor: '#00bf00',
        sliceColors: ['#007AFF', '#4CD964','#34AADC', '#FFCC00', '#fc3e39']
    });

    $("#pie-chart-2").sparkline([4,5,3,2,1], {
        type: 'pie',
        width: '150',
        height: '150',
        sliceColors: ['#007AFF', '#4CD964','#34AADC', '#FFCC00', '#fc3e39']
    });

    //work progress bar
    $("#work-progress1").sparkline([5,6,7,5,9,6,4], {
        type: 'bar',
        height: '20',
        barWidth: 5,
        barSpacing: 2,
        barColor: '#5fbf00'
    });

    $("#work-progress2").sparkline([3,2,5,8], {
        type: 'bar',
        height: '22',
        barWidth: 5,
        barSpacing: 2,
        barColor: '#4cd964'
    });

    $("#work-progress3").sparkline([1,6,9,3], {
        type: 'bar',
        height: '22',
        barWidth: 5,
        barSpacing: 2,
        barColor: '#4cd964'
    });

    $("#work-progress4").sparkline([6,7,4,3], {
        type: 'bar',
        height: '22',
        barWidth: 5,
        barSpacing: 2,
        barColor: '#34aadc'
    });

    $("#work-progress5").sparkline([6,8,5,7], {
        type: 'bar',
        height: '22',
        barWidth: 5,
        barSpacing: 2,
        barColor: '#007AFF'
    });

}();