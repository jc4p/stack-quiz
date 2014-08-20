$(function() {
    var full_list = [];
    var employee_list = [];
    var numSeen = 0;
    var curFilter = "all";

    $.get("/get-employees/", function(data) {
        full_list = data;
        employee_list = full_list.slice();

        setupInitialData();
        displayEmployee();
    });

    $(".card .front").on("click", function(e) {
        $('.card').addClass('flipped');
    });

    $(".card .back").on("click", function(e) {
        $("#employee-photo").attr("src", "");
        $('.card').removeClass('flipped');
        
        window.setTimeout(function() {
            numSeen++;
            updateScore();
            displayEmployee();
        }, 500);
    });

    $("#select-drilldown").change(function(e) {
        selection = $("#select-drilldown").val();
        if (selection != curFilter) {
            filterTo(selection);
        }
    });

    function filterTo(filter) {
        curFilter = filter;
        if (curFilter == "all") {
            employee_list = full_list.slice();
        }
        else if (curFilter == "Remote") {
            employee_list = full_list.filter(function(emp) {
                return emp['location'].indexOf("New York") == -1 
                    && emp['location'].indexOf("Denver") == -1
                    && emp['location'].indexOf("London") == -1;
            });
        }
        else {
            employee_list = full_list.filter(function(emp) {
                return emp['location'].indexOf(curFilter) != -1;
            });
        }

        setupInitialData();
        displayEmployee();
    }

    function setupInitialData() {
        numSeen = 0;
        $(".total-amount").text(employee_list.length);
        $(".seen-amount").text("0");
        updateScore();
    }

    function updateScore() {
        $(".seen-amount").text(numSeen);
    }

    var displayEmployee = function displayEmployee() {
        if(employee_list.length === 0) {
            alert("All done! Refresh to repeat.");
            return;
        }

        var currentEmployee = getRandomEmployee();

        $("#employee-photo").attr("src", currentEmployee['photo']);
        $("#employee-name").text(currentEmployee['name']);
        $("#employee-description").text(currentEmployee['position'] + " - " + currentEmployee['location']);
    };

    function getRandomEmployee() {
        var index = Math.floor(Math.random() * employee_list.length);
        return employee_list.splice(index, 1)[0];
    }
});