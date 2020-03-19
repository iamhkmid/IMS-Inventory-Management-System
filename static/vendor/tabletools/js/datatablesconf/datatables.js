$(document).ready(function() {
    
    var table = $('#datatables').DataTable( {
        "columnDefs": [{
            "targets": '_all',
            "createdCell": function (td, cellData, rowData, row, col) {
                $(td).css('padding', '7px')
            }
        }],
        buttons: [
        { extend: 'copy', className: 'btn-rounded btn-sm btn-mdb-color' },
        { extend: 'excel', className: 'btn-rounded btn-sm btn-mdb-color' },
        { extend: 'pdf', className: 'btn-rounded btn-sm btn-mdb-color' },
        { extend: 'print', className: ' btn-rounded btn-sm btn-mdb-color' },
        { extend: 'colvis', className: 'btn-rounded btn-sm btn-mdb-color' } ],
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