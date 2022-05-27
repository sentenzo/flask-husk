'use strict';
(function () {

    let ajax = function (method, url, params, callback) {
        let xhr = new XMLHttpRequest();
        if (callback) {
            xhr.onreadystatechange = function() {
                if (xhr.readyState == XMLHttpRequest.DONE) {
                    callback(xhr.response);
                }
            }
        }
        xhr.open(method, url, true);

        if (params) {
            let formData = new FormData(document.forms.person);
            for (let key in params) {
                if (params.hasOwnProperty(key)) {
                    formData.append(key, params[key]);
                }
            }
            xhr.send(formData);
        }
        else 
        {
            xhr.send();
        }
    };

    let counter = document.getElementById("counter");
    counter.set_number = function(number) {
        counter.innerText = number;
    };
    counter.get_number = function(number) {
        return Number(counter.innerText);
    };
    counter.hidden_value = 0;

    let btn_up = document.getElementById("btn_up");
    let btn_down = document.getElementById("btn_down");



    let update_counter_hidden_value = function (callback) {
        callback = callback || function() {};
        let update_counter_callback = function(response) {
            response = JSON.parse(response);
            let x = Number(response["counter"]);
            counter.hidden_value = x;
            callback();
        };
        ajax("GET", "/ajax/get_counter", false, update_counter_callback, false);

    };

    update_counter_hidden_value(() => {counter.set_number(counter.hidden_value);});

    btn_up.onclick = function() {

        let x = counter.hidden_value;
        counter.set_number(x+1);
        ajax("POST", "/ajax/inc_counter");
        update_counter_hidden_value();
    };

    btn_down.onclick = function() {
        let x = counter.hidden_value;
        counter.set_number(x-1);
        ajax("POST", "/ajax/inc_counter", {diff: -1});
        update_counter_hidden_value();
    };
})();