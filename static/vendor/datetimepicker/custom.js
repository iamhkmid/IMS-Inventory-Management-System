function setDatePicker(){
$(".datepicker").datetimepicker({
    format: 'YYYY-MM-DD HH:mm:ss.SSS'
})
}
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
                close: 'far fa-times' } });

function setDateRangePicker(input1, input2){
$(input1).datetimepicker({
    format: "YYYY-MM-DD",
    useCurrent: false
})
$(input1).on("change.datetimepicker", function (e) {
    $(input2).val("")
        $(input2).datetimepicker('minDate', e.date);
    })
$(input2).datetimepicker({
    format: "YYYY-MM-DD",
    useCurrent: false
})
}
function setMonthPicker(){
$(".monthpicker").datetimepicker({
    format: "MM",
    useCurrent: false,
    viewMode: "months"
})
}
function setYearPicker(){
$(".yearpicker").datetimepicker({
    format: "YYYY",
    useCurrent: false,
    viewMode: "years"
})
}
function setYearRangePicker(input1, input2){
$(input1).datetimepicker({
    format: "YYYY",
    useCurrent: false,
    viewMode: "years"
})
$(input1).on("change.datetimepicker", function (e) {
    $(input2).val("")
        $(input2).datetimepicker('minDate', e.date);
    })
$(input2).datetimepicker({
    format: "YYYY",
    useCurrent: false,
    viewMode: "years"
})
}