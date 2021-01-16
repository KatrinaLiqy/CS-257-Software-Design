
window.onload = initialize;

function initialize() {
    cartoon();
    table();
}


function cartoon(){
    var a = document.getElementsByClassName("words_for_pics");
    for(var i=0;i<a.length;i++){
        a[i].style.display = "block";
    }
}

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function table() {
    var url = getAPIBaseURL() + '/people_affected_all_countries';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(people_affected_all_countries) {
        var tableBody = '<tr><th>Country</th><th>Year</th><th>People Affected</th></tr>';
        for (var k = 0; k < people_affected_all_countries.length; k++) {
            var table = people_affected_all_countries[k];
            tableBody += '<tr>' + '<td>'+table['country']
                      + '</td>' + '<td>'+table['year']
                      + '</td>' + '<td>'+table['num_people_affected']
                      + '</td>' 
                      + '</tr>\n';
        }

        var people_affected_table = document.getElementById('table');
        if (people_affected_table) {
            people_affected_table.innerHTML = tableBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}







var scrollHeight = document.body.scrollHeight;
var height = window.innerHeight;
var scroll = document.getElementsByClassName("scroll")[0];

window.onscroll=function(){
　　var t =document.documentElement.scrollTop||document.body.scrollTop; 
    if(scrollHeight-4<height+t){
        scroll.style.display = "none"
    }
    else{
        scroll.style.display = "block"
    }
}

window.onresize =function(){
    height = window.innerHeight;
}