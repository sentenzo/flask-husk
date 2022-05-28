'use strict';

(function () {

    let ajax = function (method, url, params, callback) {
        let xhr = new XMLHttpRequest();
        if (callback) {
            xhr.onreadystatechange = function () {
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
        else {
            xhr.send();
        }
    };
    let server = {};
    server.sync_counter = function (callback) {
        callback = callback || function () { };
        ajax("GET", "/ajax/get_counter", false, callback);
    };

    let counter = document.getElementById("counter");
    counter.set_number = function (number) {
        counter.innerText = number;
    };
    counter.get_number = function () {
        return Number(counter.innerText);
    };

    counter._blocked_at = 0;
    counter.block = function () {
        counter._blocked_at = Date.now();
    };
    counter.is_blocked = function () {
        let delta = Date.now() - counter._blocked_at;
        return delta < 2 * 1000;
    };
    counter.unblock = function () {
        counter._blocked_at = 0;
    };

    counter._callbacks = {};
    counter._callbacks.update_counter = function (response) {
        response = JSON.parse(response);
        let x = Number(response["counter"]);
        counter.set_number(x);
        counter.unblock();
    };
    counter.update_counter = function (callback) {
        counter.block();
        callback = callback || counter._callbacks.update_counter;
        server.sync_counter(callback);
    };
    counter.inc = function (i) {
        if (counter.is_blocked()) {
            return;
        }
        counter.block();
        i = i || 1;
        ajax("POST", "/ajax/inc_counter", { diff: i }, counter._callbacks.update_counter);
        counter.set_number(counter.get_number() + i);
    };

    let btn_up = document.getElementById("btn_up");
    let btn_down = document.getElementById("btn_down");

    btn_up.onclick = () => counter.inc(1);
    btn_down.onclick = () => counter.inc(-1);

    counter.update_counter();
})();