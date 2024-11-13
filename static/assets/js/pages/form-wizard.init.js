var currentTab = 0;

function showTab(index) {
    var tabs = document.getElementsByClassName("wizard-tab");

    for (var i = 0; i < tabs.length; i++) {
        tabs[i].style.display = "none";
    }

    tabs[index].style.display = "block";

    document.getElementById("prevBtn").style.display = index === 0 ? "none" : "inline";

    var nextBtn = document.getElementById("nextBtn");
    var submitBtn = document.getElementById("submitBtn");

    if (index === tabs.length - 1) {
        nextBtn.style.display = "none";
        submitBtn.style.display = "inline";
    } else {
        nextBtn.style.display = "inline";
        submitBtn.style.display = "none";
    }

    fixStepIndicator(index);
}

function nextPrev(step) {
    var tabs = document.getElementsByClassName("wizard-tab");

    tabs[currentTab].style.display = "none";

    currentTab += step;

    if (currentTab >= tabs.length) {
        currentTab = tabs.length - 1;
    } else if (currentTab < 0) {
        currentTab = 0;
    }

    showTab(currentTab);
}

function fixStepIndicator(index) {
    var steps = document.getElementsByClassName("list-item");

    for (var i = 0; i < steps.length; i++) {
        steps[i].className = steps[i].className.replace(" active", "");
    }

    steps[index].className += " active";
}

showTab(currentTab);