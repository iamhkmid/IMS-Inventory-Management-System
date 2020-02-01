$(document).ready(function() {
  
    var table = $('#datatables2').DataTable( {
        displayLength: 10,
        lengthMenu: [[5, 10, 25, 50, 75, -1], [5, 10, 25, 50, 75, "All"]],
        scrollX: true,
        scrollY: false,
        pagingType: "full_numbers",
    } );
 
    table.buttons().container()
        .appendTo( '#datatables2_wrapper .col-md-6:eq(0)' );
} );