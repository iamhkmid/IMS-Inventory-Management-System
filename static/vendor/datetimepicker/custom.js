
$(function () {
    $('#datetimepicker1').datetimepicker({
    format: 'YYYY-MM-DD HH:mm:ss',
    vertical: 'bottom',
    horizontal: 'right',
    });
    $('#datetimepicker2').datetimepicker({
        format: 'YYYY-MM-DD HH:mm:ss',
        vertical: 'bottom',
        horizontal: 'right',
    });
});


$('#datepicker1').datetimepicker({
    format: 'YYYY-MM-DD HH:mm:ss.SSS',
    vertical: 'bottom',
    horizontal: 'right',
});
$('#datepicker3').datetimepicker({
    viewMode: 'years',
    format: 'YYYY-MM',
});

$('#datepicker4').datetimepicker({
    format: 'YYYY-MM-DD HH:mm:ss.SSS',
    vertical: 'bottom',
    horizontal: 'right',
});
$('#datepicker5').datetimepicker({  
    format: 'YYYY-MM-DD HH:mm:ss.SSS',
    vertical: 'bottom',
    sideBySide: true,
    horizontal: 'right',
});


$.fn.datetimepicker.Constructor.Default = $.extend({},
    $.fn.datetimepicker.Constructor.Default,
    { icons:
            { time: 'fas fa-clock',
                date: 'fas fa-calendar',
                up: 'fas fa-arrow-up',
                down: 'fas fa-arrow-down',
                previous: 'fas fa-arrow-circle-left',
                next: 'fas fa-arrow-circle-right',
                today: 'far fa-calendar-check-o',
                clear: 'fas fa-trash',
                close: 'far fa-times' } 
    });