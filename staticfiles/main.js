$(function() {
    var employee_list = [];

    $.get("/get-employees/", function(data) {
        employee_list = data;

        displayEmployee();
    });

    function displayEmployee() {
        random_emp = employee_list[Math.floor(Math.random() * employee_list.length)];

        $("#employee-photo").attr("src", random_emp['photo']);    
    }
});