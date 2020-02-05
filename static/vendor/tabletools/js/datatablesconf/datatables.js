$(document).ready(function() {
  
    var table = $('#datatables').DataTable( {
        buttons: [ 'copy', 'excel', 'pdf', 'print','colvis' ],
    } );
 
    table.buttons().container()
        .appendTo( '#datatables_wrapper .col-md-6:eq(0)' );
} ); 