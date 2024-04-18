function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length == 2) return parts.pop().split(";").shift();
}

function startEdit(id) {
  document.getElementById(`textarea_${id}`).style.display = "block";
  document.getElementById(`content_${id}`).style.display = "none";

  document.getElementById(`save_${id}`).style.display = "block";
  document.getElementById(`edit_${id}`).style.display = "none";
}

function submitHandler(id) {
  const textareaValue = document.getElementById(`textarea_${id}`).value;
  const content = document.getElementById(`content_${id}`);

  fetch(`/edit/${id}`, {
    method: "POST",
    headers: {
      "Content-type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      content: textareaValue,
    }),
  })
    .then((response) => response.json())
    .then((result) => (content.innerHTML = result.data));

  document.getElementById(`textarea_${id}`).style.display = "none";
  document.getElementById(`content_${id}`).style.display = "block";

  document.getElementById(`save_${id}`).style.display = "none";
  document.getElementById(`edit_${id}`).style.display = "block";
}

let addedlikedList = [];
function likeHandler(id, likedList) {
  const button = document.getElementById(`${id}`);
  const count = document.getElementById(`count_${id}`);
  addedlikedList.push(likedList);
  let liked = addedlikedList.includes(id);

  if (liked) {
    fetch(`/remove_like/${id}`)
      .then((response) => response.json())
      .then((result) => {
        if (button.classList.contains("fa-solid")) {
          button.classList.add("fa-regular");
          button.classList.remove("fa-solid");
        } else {
          button.classList.add("fa-solid");
          button.classList.remove("fa-regular");
        }
        count.innerHTML = result.counter;
        addedlikedList.splice(addedlikedList.indexOf(id), 1);
        console.log(result);
      });
  } else {
    fetch(`/add_like/${id}`)
      .then((response) => response.json())
      .then((result) => {
        if (button.classList.contains("fa-solid")) {
          button.classList.add("fa-regular");
          button.classList.remove("fa-solid");
        } else {
          button.classList.add("fa-solid");
          button.classList.remove("fa-regular");
        }
        count.innerHTML = result.counter;
        addedlikedList.push(id);
        console.log(result);
      });
  }
}
