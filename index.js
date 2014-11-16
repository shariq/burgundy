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
        hmmDotting()
    }, 300);

    function changeWord() {
        $.get('http://burgundy.io:8080/', function(data) {
            loaded[0] = 0;
            $('#suggestion')[0].textContent = data;
            clearInterval(intervalVar);
        });
    }

    changeWord();

//    $('#suggestion')[0].bigtext();

    $(document).keypress(changeWord);
    $(document).click(changeWord);
    $('body')[0].tap(changeWord);
    $('body')[0].swipe(changeWord);
});
