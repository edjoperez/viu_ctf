function makeAjaxCall(method, url, data, successCallback, errorCallback) {
    const xhr = new XMLHttpRequest();
  
    xhr.open(method, url);
    xhr.setRequestHeader('Content-Type', 'application/json'); // Adjust if needed
  
    xhr.onload = function() {
      if (xhr.status >= 200 && xhr.status < 300) {
        const responseData = JSON.parse(xhr.responseText); // Assuming JSON response
        successCallback(responseData);
      } else {
        errorCallback(xhr.statusText);
      }
    };
  
    xhr.onerror = function() {
      errorCallback('Network error');
    };
  
    xhr.send(JSON.stringify(data)); // Send data if provided
  }

  //TODO: Not going to be implemented in v1.0

  //service: 
  // /v1/posts/create
  // GET
  // CTF
  // flag{f1rSt_C7F_cH@113n93}