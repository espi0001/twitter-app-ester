// For ajax.html
async function tweet() {
  // by default it's af GET
  const connection = await fetch("/tweet") // tweet is a endpoint we made up 
  const dataFromServer = await connection.text() // the empolyee that grab the data from the server and brings it back
  console.log(dataFromServer);
  document.querySelector('#message').innerHTML = dataFromServer;
}


// For ajax_post.html
async function save() {
  // If other methods (anything but GET) are needed, use the second argument.
  console.log(event) // click (will show the event -> lick { target: button, buttons: 0, clientX: 229, clientY: 98, layerX: 229, layerY: 98 })
  console.log(event.target) // button (will show where the event happens - button)
  console.log(event.target.form) // form (will show the form)

  const theForm = event.target.form
  const connection = await fetch("/save", { 
    method: "POST", // second argument is a json object
    body: new FormData(theForm)
  }) 
  //const dataFromServer = await connection.text()
  const dataFromServer = await connection.json()
  console.log(dataFromServer);
  document.querySelector('#saveMessage').innerHTML = `Hi ${dataFromServer.user_name} ${dataFromServer.user_last_name} ${dataFromServer.user_nick_name}`;
}


// For ajax_heart.html
async function likeTweet() {
  console.log("like tweet")
  const conn = await fetch("/api-like-tweet")
  if (conn.ok) {
    // if the connection went okay
    const data = await conn.json() // Get the data back as JSON
    document.querySelector("#like_tweet").classList.toggle("hidden") // we want to hide the button and then display the other button
    document.querySelector("#unlike_tweet").classList.toggle("hidden") // we want to hide the button and then display the other button
  } else {
    // if the connection did not work
    console.log("error")
  }
  
}
async function unlikeTweet() {
  console.log("unlike tweet")
  const conn = await fetch("/api-unlike-tweet")
  if (conn.ok) {
    // if the connection went okay
    const data = await conn.json() // Get the data back as JSON
    document.querySelector("#like_tweet").classList.toggle("hidden") 
    document.querySelector("#unlike_tweet").classList.toggle("hidden")
  } else {
    // if the connection did not work
    console.log("error")
  }
  
}





// udkommenteret d. 30.09
// const burger = document.querySelector(".burger");
// const nav = document.querySelector("nav");

// burger.addEventListener("click", () => {
//   // toggle nav
//   nav.classList.toggle("active");

//   // toggle icon
//   burger.classList.toggle("open");
// });
