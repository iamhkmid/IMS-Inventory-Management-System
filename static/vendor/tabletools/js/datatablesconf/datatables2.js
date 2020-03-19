$(document).ready(function() {
  
    var table = $('#datatables2').DataTable( {
        displayLength: 10,
        lengthMenu: [[5, 10, 25, 50, 75, -1], [5, 10, 25, 50, 75, "All"]],
        pagingType: "full_numbers",
        "columnDefs": [{
            "targets": '_all',
            "createdCell": function (td, cellData, rowData, row, col) {
                $(td).css('padding', '10px')
            }
        }],
    } );
 
    table.buttons().container()
        .appendTo( '#datatables2_wrapper .col-md-6:eq(0)' );
} );