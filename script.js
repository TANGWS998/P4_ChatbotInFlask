var generateButton = document.getElementById('generate');
var fruitBox = document.getElementById('fruit');
var responseButton = document.getElementById('get_response');
var queryBox = document.getElementById('query');
var responseBox = document.getElementById('response');

generateButton.addEventListener('click', function(){
    fetch('http://localhost:8010/proxy/fruit')
    .then(response => response.json())
    .then(data =>{
        fruit = data.fruit;
        fruitBox.value = fruit;
    });
})

//Fetch the response from API
async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

responseButton.addEventListener('click', async function(){
    await postData('http://localhost:8010/proxy/chat', {"query":queryBox.value})
    .then(data =>{
        response = data.response;
        responseBox.value = response;
    });
})

