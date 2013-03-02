$(document).ready(function () {
    /*
     * Responsive chart
     */
    $(window).on('resize', function () {
        chart = $('.chart svg');

        console.log('chart', chart);
        console.log('chart parent', chart.parent(), chart.parent().width(),
                    chart.parent().height());

        chart.attr('width', chart.parent().width());
        chart.attr('height', chart.parent().width() * 0.53);
    });
});
