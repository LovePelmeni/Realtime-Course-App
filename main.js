// got an idea to replace btn value with courses queryset.....
valid_codes = [200, 201, 202, 203, 204, 205]
btn_data = document.getElementById('btn').value;

var count;
SendParseTaskRequest();

btn.addEventListener('click', function(event){

    console.log('started...');
    btn.innerHTML = 'Close Course';

    start();
    // start point of the mechanism.....
    course_name = document.getElementById('course_name');
    course_amount = document.getElementById('course_amount');

    var url = new URL('http://127.0.0.1:8000/events/');
    url.searchParams.append('channel', 'course');
    var source = new ReconnectingEventSource(url);

    if (count == 1){

        sendStreamDataRequest(true);
        source.close();
        console.log('canceled.....');
        btn.innerHTML = 'Get Course';
    }

    source.onopen = function(event){
        console.log('Source has been connected....', event);
        console.log(source, 'this is source on open.....');
        count = 1;
        sendStreamDataRequest(false);
    };

    console.log(source, source.url, source.readyState);

    source.addEventListener('message', function(event){

        console.log('message has been received....');
        data = JSON.parse(event.data);
        console.log(data);

        for (var key in data){
            course_name.innerHTML = key;
            course_amount.innerHTML = data[key];
        }

    }, false);

    source.onerror = function(err) {
      console.error("EventSource failed:", err);
      source.close();
    };
});

function SendParseTaskRequest(){

    console.log('sending request...')
    var url = new URL('http://127.0.0.1:8000/handle/parse/task/')
    url.searchParams.append('list_of_courses', btn_data);
    console.log(btn_data);

    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.send();
    console.log('request has been sended.....');
}

function start() {
  if (!window.EventSource) {
    alert("This site is not available in this browser");
    return;
  } else{
    console.log('OK...')
  }
}

function sendStreamDataRequest(stop){

    var request = new XMLHttpRequest();
    var url = new URL('http://127.0.0.1:8000/send/stream/data/');

    if (stop == true){
        url.searchParams.append('stop', true);
    }
    request.open('GET', url, true);
    request.send();
}





