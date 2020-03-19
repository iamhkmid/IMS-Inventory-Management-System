$(document).ready(function() {
  
    var table = $('#datatables3').DataTable( {
        "columnDefs": [{
            "targets": '_all',
            "createdCell": function (td, cellData, rowData, row, col) {
                $(td).css('padding', '10px')
            }
        }],
    } );
    $('#datatables_wrapper .dataTables_filter').find(
        'input').each(function () {
        $('input').attr("placeholder", "Type here ..");
      });
      $('#datatables_wrapper .dataTables_filter').addClass(
        'md-form');
    
    $('#datatables_wrapper .dataTables_filter').addClass('align-right');
    table.buttons().container()
        .appendTo( '#datatables_wrapper .col-md-6:eq(0)' );
        
    
} ); 