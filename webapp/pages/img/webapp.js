/*
 * webapp.js
 * Jeff Ondich
 * 6 November 2020
 *
 * A little bit of Javascript for the tiny web app sample for CS257.
 */

window.onload = initialize;

function initialize() {
    var element = document.getElementById('cats_button');
    if (element) {
        element.onclick = onCatsButton;
    }
}

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function onCatsButton() {
    var url = getAPIBaseURL() + '/people_affected_all_countries';

    fetch(url, { method: 'get' })

        .then((response) => response.json())

        .then(function (people_affected_all_countries) {
            var listBody = '';
            for (var k = 0; k < cats.length; k++) {
                var cat = cats[k];
                listBody += '<li>' + cat['name']
                    + ', ' + cat['birth_year']
                    + '-' + cat['death_year']
                    + ', ' + cat['description'];
                + '</li>\n';
            }

            var animalListElement = document.getElementById('animal_list');
            if (animalListElement) {
                animalListElement.innerHTML = listBody;
            }
        })

        .catch(function (error) {
            console.log(error);
        });
}