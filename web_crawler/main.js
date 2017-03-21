/*$(document).ready(function() {
    $('li').click(function() {
        $('.tab').hide().eq($(this).index()).show();
        $('ul.tabs li').removeClass('current');
        $(this).addClass('current');
    });
});*/


function showTabs(elem) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName('tabContent')
    for  ( i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = 'none';
    }

    document.getElementsByClassName(elem.id)[0].style.display = 'block';

    tablinks = document.getElementsByClassName('tablink');
    for (i=0; i < tablinks.length; i++) {
        tablinks[i].style.color = 'black';
    }
    elem.style.color = '#cc3333';

}









