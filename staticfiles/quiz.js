$(function() {
    var common_last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson", "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White", "Lopez", "Lee", "Gonzalez", "Harris", "Clark", "Lewis", "Robinson", "Walker", "Perez", "Hall", "Young", "Allen", "Sanchez", "Wright", "King", "Scott", "Green", "Baker", "Adams", "Nelson", "Hill", "Ramirez", "Campbell", "Mitchell", "Roberts", "Carter", "Phillips", "Evans", "Turner", "Torres", "Parker", "Collins", "Edwards", "Stewart", "Flores", "Morris", "Nguyen", "Murphy", "Rivera", "Cook", "Rogers", "Morgan", "Peterson", "Cooper", "Reed", "Bailey", "Bell", "Gomez", "Kelly", "Howard", "Ward", "Cox", "Diaz", "Richardson", "Wood", "Watson", "Brooks", "Bennett", "Gray", "James", "Reyes", "Cruz", "Hughes", "Price", "Myers", "Long", "Foster", "Sanders", "Ross", "Morales", "Powell", "Sullivan", "Russell", "Ortiz", "Jenkins", "Gutierrez", "Perry", "Butler", "Barnes", "Fisher"];
    var male_first_names = [];
    var female_first_names = [];

    var full_list = [];
    var employee_list = [];
    var currentEmployee;
    var currentCorrectAnswer;
    var numSuccess = 0;
    var numFailure = 0;
    var curFilter = "all";

    $.get("/get-employees/", function(data) {
        full_list = data;
        employee_list = full_list.slice();

        setupInitialData();
        displayEmployee();
    });
    
    $("#select-drilldown").change(function(e) {
        selection = $("#select-drilldown").val();
        if (selection != curFilter) {
            filterTo(selection);
        }
    });

    $(".btn-default").on("click", function(e) {
        index = $(e.currentTarget).data("index");
        if(index == String(currentCorrectAnswer)) {
            numSuccess++;
            showSuccess();
        }
        else {
            numFailure++;
            showFailure();
        }

        updateScore();

        window.setTimeout(displayEmployee, 1000);
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
                return emp['location'].indexOf(curFilter) > -1;
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
        updateScore();
    }

    function showSuccess() {
        $("#response-success").slideDown(250, function() {
            window.setTimeout(function() {
                $("#response-success").slideUp(250);
            }, 500);
        });
    }

    function showFailure() {
        $("#response-failure .correct-response").text(currentEmployee['name']);
        $("#response-failure").slideDown(250, function() {
            window.setTimeout(function() {
                $("#response-failure").slideUp(250);
            }, 500);
        });
    }

    function updateScore() {
        $(".success-amount").text(numSuccess);
        $(".failure-amount").text(numFailure);
    }

    var displayEmployee = function displayEmployee() {
        if(employee_list.length === 0) {
            alert("All done!");
            return;
        }

        currentEmployee = getRandomEmployee();

        $("#employee-photo").attr("src", currentEmployee['photo']);

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