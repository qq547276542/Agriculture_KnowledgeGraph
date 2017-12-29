var Sliders = function () {

    // default sliders
    $("#default-slider").slider();

    // increment
    $("#increment-slider").slider({
        value: 10,
        min: 0,
        max: 100,
        step: 10,
        slide: function (event, ui) {
            $("#increment-slider-amount").text("$" + ui.value);
        }
    });
    $("#increment-slider-amount").text("$" + $("#increment-slider").slider("value"));

    // range slider
    $("#slider-range").slider({
        range: true,
        min: 0,
        max: 1000,
        values: [100, 400],
        slide: function (event, ui) {
            $("#slider-range-amount").text("$" + ui.values[0] + " - $" + ui.values[1]);
        }
    });

    $("#slider-range-amount").text("$" + $("#slider-range").slider("values", 0) + " - $" + $("#slider-range").slider("values", 1));

    //range max
    $("#slider-range-max").slider({
        range: "max",
        min: 1,
        max: 100,
        value: 15,
        slide: function (event, ui) {
            $("#slider-range-max-amount").text("$" + ui.value);
        }
    });

    $("#slider-range-max-amount").text($("#slider-range-max").slider("value"));

    // range min
    $("#slider-range-min").slider({
        range: "min",
        value: 55,
        min: 1,
        max: 100,
        slide: function (event, ui) {
            $("#slider-range-min-amount").text("$" + ui.value);
        }
    });
    $("#slider-range-min-amount").text("$" + $("#slider-range-min").slider("value"));

    
    // setup graphic EQ
    $( "#eq > span" ).each(function() {    
        var value = parseInt( $( this ).text(), 10 );
        $( this ).empty().slider({
            value: value,
            range: "min",
            animate: true,
            orientation: "vertical"
        });
    });

    // bound to select
    var select = $( "#bound-to-select" );
    var slider = $( "<div id='slider'></div>" ).insertAfter( select ).slider({
        min: 1,
        max: 10,
        range: "min",
        value: select[ 0 ].selectedIndex + 1,
        slide: function( event, ui ) {
            select[ 0 ].selectedIndex = ui.value - 1;
        }
    });
    $( "#bound-to-select" ).change(function() {
        slider.slider( "value", this.selectedIndex + 1 );
    });

    // vertical slider
    $("#slider-vertical").slider({
        orientation: "vertical",
        range: "min",
        min: 0,
        max: 100,
        value: 40,
        slide: function (event, ui) {
            $("#slider-vertical-amount").text(ui.value+" cm");
        }
    });
    $("#slider-vertical-amount").text($("#slider-vertical").slider("value")+" cm");

    // vertical range sliders
    $("#slider-range-vertical").slider({
        orientation: "vertical",
        range: true,
        min: 0,
        max: 1000,
        values: [200, 600],
        slide: function (event, ui) {
            $("#slider-range-vertical-amount").text("$" + ui.values[0] + " - $" + ui.values[1]);
        }
    });

    $("#slider-range-vertical-amount").text("$" + $("#slider-range-vertical").slider("values", 0) + " - $" + $("#slider-range-vertical").slider("values", 1));


}();