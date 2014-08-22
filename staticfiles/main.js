$(function() {
    var full_list = [];
    var employee_list = [];
    var wrong_list = [];
    var numSeen = 0;
    var numRight = 0;
    var curFilter = "all";
    var currentEmployee;

    $.get("/get-employees/", function(data) {
        full_list = data;
        employee_list = full_list.slice();

        setupInitialData();
        displayEmployee();
    });

    $(".card .front").on("click", function(e) {
        $('.card').addClass('flipped');
        
        window.setTimeout(function() {
            $("#response-container").show();
        }, 400);
    });

    $("#select-drilldown").change(function(e) {
        selection = $("#select-drilldown").val();
        if (selection != curFilter) {
            filterTo(selection);
        }
    });
    
    $(document).keyup(function(e) {
        if (e.keyCode == 32) { // space bar
            if (!$("#response-container").is(":visible")) {
                // if the card isn't flipped, flip it
                $(".card .front").click();
            }
        }
    });

    $("#button-right").on("click", function(e) {
       numRight++;
       showNext();
    });
    
    $("#button-wrong").on("click", function(e) {
        wrong_list.push(currentEmployee);
        showNext(); 
    });
    
    function showNext() {
        $("#response-container").hide();
        $("#employee-photo").attr("src", "");
        $('.card').removeClass('flipped');
        window.setTimeout(function() {
            numSeen++;
            updateScore();
            displayEmployee();
        }, 500);
    }

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
                return emp['location'].indexOf(curFilter) > -1;
            });
        }

        setupInitialData();
        displayEmployee();
    }

    function setupInitialData() {
        numSeen = 0;
        $(".total-amount").text(employee_list.length);
        $(".correct-amount").text("0");
        updateScore();
    }

    function updateScore() {
        $(".correct-amount").text(numRight);
    }

    var displayEmployee = function displayEmployee() {
        if(employee_list.length === 0) {
            showEnd();
            return;
        }

        currentEmployee = getRandomEmployee();

        $("#employee-photo").attr("src", currentEmployee['photo']);
        $("#employee-name").text(currentEmployee['name']);
        $("#employee-description").text(currentEmployee['position'] + " - " + currentEmployee['location']);
    };

    function getRandomEmployee() {
        var index = Math.floor(Math.random() * employee_list.length);
        return employee_list.splice(index, 1)[0];
    }
    
    function showEnd() {
        $(".card-container").hide();
        $("#end-container").show();
        
        if (wrong_list.length == 0) {
            $("#summary").text("Wow, you got every one of them right!");
        }
        else {
            $("#summary").html("You missed " + wrong_list.length + " people:<br>");
            for(i = 0; i < wrong_list.length; i++) {
                $("#summary").append(wrong_list[i]['name'] + "<br>");
            }
        }
    }
});