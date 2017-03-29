
function showTabs(elem) {
    var tabcontent = document.getElementsByClassName("tab_content")
    for  ( var i = 0; i < tabcontent.length; i++) {
        tabcontent[i].classList.remove("current");
    }

    var tab = elem.getAttribute("data-tab");
    document.getElementById(tab).classList.add("current");

    var tablinks = document.getElementsByClassName("tablink");
    for (i=0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("selected");
    }
    elem.classList.add("selected");

};


function get_modal(id) {
    var url = document.getElementById(id).innerText;
    var modal =  document.getElementById("my_modal").style.display = "block";
    document.getElementById("source").value = url;
    var id_field = document.getElementById("source_id");
    id_field.value = id.slice(4)
};

function editClose() {
    document.getElementById("my_modal").style.display = "none";
};

function editUrl() {
    var url = document.getElementById("source").value;
    var url_id = document.getElementById("source_id").value;
    document.getElementById("url_" + url_id).innerHTML=url;
    editClose();

};

function status_button(elem) {
    var class_list = elem.classList;
    if (class_list.contains("status_btn_on")) {
        class_list.remove("status_btn_on");
        class_list.add("status_btn_off");
    } else {
        class_list.remove("status_btn_off");
        class_list.add("status_btn_on");
    }
};








