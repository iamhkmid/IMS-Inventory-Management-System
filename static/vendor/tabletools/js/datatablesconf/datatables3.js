$(document).ready(function() {
  
    var table = $('#datatables3').DataTable( {
        responsive: true,
        autoWidth : true,
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

    $('#datatables3 tbody tr').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);
        var child = table.row( this ).child;
    
        if (row.child.isShown()) {
            // This row is already open - close it
            child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            child.show();
            tr.addClass('shown');
        }
 
        
    });

} );