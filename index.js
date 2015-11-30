$(document).ready(function() {

    var loaded = [4];
    var intervalVar;

    function hmmDotting() {
        if (loaded[0] > 0) {
            $('#suggestion')[0].textContent = 'hmm' + ['', '.', '..', '...'][4 - loaded[0]];
            loaded[0] = loaded[0] - 1;
        } else {
            clearInterval(intervalVar);
        }
    }

    intervalVar = window.setInterval(function() {
        hmmDotting();
    }, 300);

    function changeWord() {
        $.get('http://burgundy.io:8080/', function(data) {
            loaded[0] = 0;
            $('#suggestion')[0].textContent = data;
            clearInterval(intervalVar);
        });
    }

    document.body.addEventListener("mousedown", tapOrClick, false);
    document.body.addEventListener("touchstart", tapOrClick, false);

    function tapOrClick(event) {
        changeWord();

        event.preventDefault();
        return false;
    }

    changeWord();

    var down = {};

    $(document).keydown(function(event){
        if (down['q'] == null) {
            changeWord();
            down['q'] = true;
        }
    });

    $(document).keyup(function(event) {
        down['q'] = null;
    });

});
