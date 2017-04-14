$(document).ready(function () {
        $("#slider").slider({
            range: "min",
            animate: true,
            value: 1,
            min: 1950,
            max: 2100,
            step: 1,
            slide: function (event, ui) {
                update(1, ui.value); //changed
            }
        });

        //Added, set initial value.
        $("#amount").val(0);
        $("#amount-label").text(0);


        update();
    });

    //changed. now with parameter
    function update(slider, val) {
        //changed. Now, directly take value from ui.value. if not set (initial, will use current value.)
        var $amount = slider == 1 ? val : $("#amount").val();

        /* commented
         $amount = $( "#slider" ).slider( "value" );
         $duration = $( "#slider2" ).slider( "value" );
         */

        $("#amount").val($amount);
        $("#amount-label").text($amount);

        $('#slider a').html('<label>' + $amount + '</label><div class="ui-slider-label-inner"></div>');
    }