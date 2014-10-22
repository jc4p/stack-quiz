var common_last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson", "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White", "Lopez", "Lee", "Gonzalez", "Harris", "Clark", "Lewis", "Robinson", "Walker", "Perez", "Hall", "Young", "Allen", "Sanchez", "Wright", "King", "Scott", "Green", "Baker", "Adams", "Nelson", "Hill", "Ramirez", "Campbell", "Mitchell", "Roberts", "Carter", "Phillips", "Evans", "Turner", "Torres", "Parker", "Collins", "Edwards", "Stewart", "Flores", "Morris", "Nguyen", "Murphy", "Rivera", "Cook", "Rogers", "Morgan", "Peterson", "Cooper", "Reed", "Bailey", "Bell", "Gomez", "Kelly", "Howard", "Ward", "Cox", "Diaz", "Richardson", "Wood", "Watson", "Brooks", "Bennett", "Gray", "James", "Reyes", "Cruz", "Hughes", "Price", "Myers", "Long", "Foster", "Sanders", "Ross", "Morales", "Powell", "Sullivan", "Russell", "Ortiz", "Jenkins", "Gutierrez", "Perry", "Butler", "Barnes", "Fisher"];
var male_first_names = [];
var female_first_names = [];

var employee_list = [];
var full_list = [];
var wrong_list = [];
var currentEmployee;
var currentCorrectAnswer;
var numSuccess = 0;
var numFailure = 0;
var locationFilter = "all";
var departmentFilter = "all";


$(function() {
    $.get("/get-employees/", function(data) {
        full_list = data;
        employee_list = full_list.slice();

        setupInitialData();
        displayEmployee();
    });
    
    $("#location-drilldown").change(function(e) {
        selection = $("#location-drilldown").val();
        if (selection != locationFilter) {
            locationFilter = selection;
            filterTo();
        }
    });

    $("#department-drilldown").change(function(e) {
        selection = $("#department-drilldown").val();
        if (selection != departmentFilter) {
            departmentFilter = selection;
            filterTo();
        }
    });

    $("#filters-toggle").on("click", function(e) {
        $("#filters-container").slideToggle();
    });

    $(".btn-default").on("click", function(e) {
        index = $(e.currentTarget).data("index");
        wasCorrect = true;
        if(index == String(currentCorrectAnswer)) {
            numSuccess++;
        }
        else {
            wrong_list.push(currentEmployee);
            numFailure++;
            wasCorrect = false;
        }

        updateScore();
        showResult(wasCorrect);
        $(".card").addClass("flipped");
    });

    $(".card .back").on("click", function(e) {
        displayEmployee();
        $(".card").removeClass("flipped");
    });
    
    function filterTo() {
        // Location first
        if (locationFilter == "all") {
            employee_list = full_list.slice();
        }
        else if (locationFilter == "Remote") {
            employee_list = full_list.filter(function(emp) {
                return emp['location'].indexOf("New York") == -1 
                    && emp['location'].indexOf("Denver") == -1
                    && emp['location'].indexOf("London") == -1;
            });
        }
        else {
            employee_list = full_list.filter(function(emp) {
                return emp['location'].indexOf(locationFilter) > -1;
            });
        }

        // Then Department
        if (departmentFilter != "all") {
            employee_list = employee_list.filter(function(emp) {
                return emp['department'] == departmentFilter;
            });
        }

        setupInitialData();
        displayEmployee();
    }

    function setupInitialData() {
        for(var indx in full_list) {
            var gender = full_list[indx]['gender'];
            var name_split = full_list[indx]['name'].split(" ");
            var first_name = name_split[0];

            if (gender === "M") {
                male_first_names.push(first_name);
            }
            else {
                female_first_names.push(first_name);
            }
        }
        $(".total-amount").text(employee_list.length);
        numSuccess = 0;
        numFailure = 0;
        updateScore();
    }

    function showResult(wasCorrect) {
        $("#employee-photo-back").attr("src", currentEmployee['photo']);
        $("#employee-description").text(currentEmployee['position'] + " - " + currentEmployee['location']);
        if (currentEmployee.hasOwnProperty("nickname")) {
            firstName = currentEmployee['name'].split(" ")[0]
            rest = currentEmployee['name'].substring(firstName.length + 1);

            $("#employee-name").text(firstName + " \"" + currentEmployee['nickname'] + "\" " + rest);
        }
        else {
            $("#employee-name").text(currentEmployee['name']);
        }

        if (wasCorrect) {
            $("#employee-name").addClass("correct");
        }
        else {
            $("#employee-name").removeClass("correct");
        }
    }

    function updateScore() {
        $(".success-amount").text(numSuccess);
        $(".failure-amount").text(numFailure);
    }

    var displayEmployee = function displayEmployee() {
        if(employee_list.length === 0) {
            showEnd();
            return;
        }

        currentEmployee = getRandomEmployee();

        $("#employee-photo-front").attr("src", currentEmployee['photo']);

        var otherNames = getNRandomNamesOtherThan(currentEmployee, 10);

        var names = [currentEmployee['name']];
        for(var indx in otherNames) {
            names.push(otherNames[indx]);
        }

        names = shuffle(names);

        for(var i in names) {
            if (names[i] == currentEmployee['name']) {
                currentCorrectAnswer = i;
                break;
            }
        }

        // If the correct answer is out of the set we're going to actually show
        // force it back into the set.
        if(parseInt(currentCorrectAnswer) > 2) {
            currentCorrectAnswer = Math.floor(Math.random() * 3);
            names[currentCorrectAnswer] = currentEmployee['name'];
        }

        $("#option-a").text(names[0]);
        $("#option-b").text(names[1]);
        $("#option-c").text(names[2]);
    };

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

    function getNRandomNamesOtherThan(employee, n) {
        var names = [];

        while(names.length <= n) {
            thisName = generateRandomName(employee['gender'], employee['name']);
            names.push(thisName);
        }

        return names;
    }

    function generateRandomName(gender, forbidden_name) {
        var first_name = getRandomFirstNameByGender(gender);
        var last_name = getRandomLastName();

        if(first_name == forbidden_name.split(" ")[0]) {
            return generateRandomName(gender, forbidden_name);
        }
        
        return first_name + " " + last_name;
    }

    function getRandomFirstNameByGender(gender) {
        if (gender == "M") {
            return male_first_names[Math.floor(Math.random() * male_first_names.length)];    
        }

        return female_first_names[Math.floor(Math.random() * female_first_names.length)];
    }

    function getRandomLastName() {
        return common_last_names[Math.floor(Math.random() * common_last_names.length)];
    }

    // deprecated
    function getNNamesOtherThan(employee, n) {
        var names = [];

        while(names.length <= n) {
            thisName =  getRandomEmployeeFromAllByGender(employee['gender'])['name'];
            if(thisName != employee['name'] && names.indexOf(thisName) == -1) {
                names.push(thisName);
            }
        }

        return names;
    }

    function getRandomEmployee() {
        var index = Math.floor(Math.random() * employee_list.length);
        return employee_list.splice(index, 1)[0];
    }

    // deprecated
    function getRandomEmployeeFromAllByGender(gender) {
        emp = full_list[Math.floor(Math.random() * full_list.length)];

        if(emp['gender'] !== gender) {
            return getRandomEmployeeFromAllByGender(gender);
        }
        
        return emp;
    }

    // http://stackoverflow.com/a/6274398/472021
    // There's something ironic about this comment being in a Stack-related app.
    function shuffle(array) {
        var counter = array.length, temp, index;

        // While there are elements in the array
        while (counter--) {
            // Pick a random index
            index = (Math.random() * counter) | 0;

            // And swap the last element with it
            temp = array[counter];
            array[counter] = array[index];
            array[index] = temp;
        }

        return array;
    }
});