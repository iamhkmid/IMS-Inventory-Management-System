$(document).ready(function() {
  
    var table = $('#datatables3').DataTable( {
        rowReorder: {
            selector: 'td:nth-child(2)'
        },
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

    $('#datatables').on('click', 'button', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
        } else {
            // Open this row
            tr.addClass('shown');
        }
    });

} );