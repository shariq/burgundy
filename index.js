$(document).ready(function() {

var loaded = [4];
var intervalVar;

function hmming() {
  if (loaded[0] > 0) {
    $('#suggestion')[0].textContent = 'hmm'+['','.','..','...'][4-loaded[0]];
    loaded[0] = loaded[0] - 1;
  }
  else {
    clearInterval(intervalVar);
  }
}

intervalVar = window.setInterval(function() {hmming()}, 300);

$.get('http://burgundy.io:8080/', function(data) {
  loaded[0] = 0;
  $('#suggestion')[0].textContent = data;
});

});
