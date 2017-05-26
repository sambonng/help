$(document).ready(function(){

	$(".tr-btn").on('click',function(){
        clickEvent($(this));
    });

    $("#reset-btn").click(function(){
        $('#select-table > tbody > tr').remove();
        $('.tr-btn').off('click').on('click', function(){
            clickEvent($(this));
        });
    });
});

function doTheSubmit() {
    var approvals = $('#select-table tbody').children();
    var doc = window.opener.document;
    if(!approvals.length){
        alert('결재자를 지정해 주십시오!');
        return;
    }
    var i = 1;
    userId = approvals.each(function(){
        var value = $(this).find($('td:nth-child(2)')).attr('id-data');
        var str = 'n'+i;
        field = doc.getElementById(str);
        field.value = value;
        i++;
    });
    doc.getElementById('counselForm').submit();
    window.close();

}


function clickEvent(Object){
    var html = Object.parents('tr').html();
    Object.off('click');
    html = '<td></td>' + html;
    $('#select-table tbody').prepend('<tr>'+html+'</tr>');
    $('#select-table tbody').remove('.tr-btn');
    var i=1;
    $('#select-table tbody tr').each(function(){
        if(i == 1){
            $(this).children(":first").text('최종 결재자');
        }
        else $(this).children(":first").text(i);
        i++;
    });
}
