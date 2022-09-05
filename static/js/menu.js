function closeNav() {

    // $(".openbtn_header" ).removeClass( "openbtn-header-nav" );
    // $(".span_name_menu" ).removeClass( "span_name_menu-nav" );
    document.getElementById("openbtn").style.background = "#ffffff";
    document.getElementById("a_closebtn_header").style.display = "none";
    document.getElementById("mySidebar").style.width = "80px";
    document.getElementById("span_name_menu_1").style.display = "none";
    document.getElementById("span_name_menu_2").style.display = "none";
    document.getElementById("span_name_menu_3").style.display = "none";
    document.getElementById("span_name_menu_4").style.display = "none";
    document.getElementById("span_name_menu_5").style.display = "none";
    document.getElementById("span_name_menu_6").style.display = "none";
    document.getElementById("span_name_menu_7").style.display = "none";
    // document.getElementsByClassName("span_name_menu").style.display = "none";
    // document.getElementById("main").style.marginLeft = "0";

}

function openNav() {

    document.getElementById("mySidebar").style.width = "230px";
    // document.getElementById("main").style.display = "block";
    document.getElementById("a_closebtn_header").style.display = "block";
    document.getElementById("openbtn").style.background = "#0232A0";
    // document.getElementsByClassName("span_name_menu").style.display = "block";
    document.getElementById("span_name_menu_1").style.display = "block";
    document.getElementById("span_name_menu_2").style.display = "block";
    document.getElementById("span_name_menu_3").style.display = "block";
    document.getElementById("span_name_menu_4").style.display = "block";
    document.getElementById("span_name_menu_5").style.display = "block";
    document.getElementById("span_name_menu_6").style.display = "block";
    document.getElementById("span_name_menu_7").style.display = "block";
    // $( ".span_name_menu" ).addClass( "myClass yourClass" );
    // $(".openbtn_header").addClass( "openbtn-header-nav" );
    // $(".span_name_menu").addClass( "span_name_menu-nav" );
    // $("#a_closebtn_header" ).addClass( "closebtn-opent" );
}