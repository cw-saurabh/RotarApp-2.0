let active = 'Admin';
function openSection(sectionName) {
    active=sectionName;
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++)
    {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++)
    {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    // document.getElementById(sectionName).style.display = "block";
    // evt.currentTarget.className += " active";
    document.getElementById(sectionName+"Link").className+= " active";
    document.getElementById(sectionName).style.display = "block";
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

function openPrevSection() {
    if (active == 'Admin')
    openSection('Others');
    else if (active == 'Avenue')
    openSection('Admin');
    else if (active == 'Others')
    openSection('Avenue');
}

function openNextSection() {
    if (active == 'Admin')
    openSection('Avenue');
    else if (active == 'Avenue')
    openSection('Others');
    else if (active == 'Others')
    openSection('Admin');
}

