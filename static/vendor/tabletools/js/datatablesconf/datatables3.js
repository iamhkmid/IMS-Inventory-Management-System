$(document).ready(function() {
  
    var table = $('#datatables3').DataTable( {
        displayLength: 5,
        lengthMenu: [[5, 10, 25, 50, 75, -1], [5, 10, 25, 50, 75, "All"]],
        pagingType: "full_numbers",
        "columnDefs": [{
            "targets": '_all',
            "createdCell": function (td, cellData, rowData, row, col) {
                $(td).css('padding', '10px')
            }
        }],
    } );
} );