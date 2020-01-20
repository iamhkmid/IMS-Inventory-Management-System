$(document).ready(function() {
  
    var table = $('#datatables').DataTable( {
        displayLength: 10,
        lengthMenu: [[5, 10, 25, 50, 75, -1], [5, 10, 25, 50, 75, "All"]],
        scrollX: true,
        scrollY: false,
        pagingType: "full_numbers",
        buttons: [ 'copy', 'csv', 'excel', 'pdf', 'print' ]
    } );
 
    table.buttons().container()
        .appendTo( '#datatables_wrapper .col-md-6:eq(0)' );
} );