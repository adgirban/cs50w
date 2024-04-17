document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));

  document.querySelector("#compose").addEventListener("click", compose_email);
  //Submit the email
  document
    .querySelector("#compose-form")
    .addEventListener("submit", send_email);

  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";
  document.querySelector("#emails-detail-view").style.display = "none";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#emails-detail-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  //Get the emails
  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      emails.forEach((email) => {
        const element = document.createElement("div");
        element.innerHTML = `<div class="email">` + email.sender + `</div>`;
        element.innerHTML += `<div class="email">` + email.subject + `</div>`;
        element.innerHTML += `<div class="email">` + email.timestamp + `</div>`;

        if (mailbox === "inbox") {
          const archiveButton = document.createElement("button");
          archiveButton.innerHTML = "Archive";
          archiveButton.classList.add(
            "btn-secondary",
            "btn-sm",
            "btn-outline-dark"
          );
          archiveButton.style.color = "black";
          archiveButton.addEventListener("click", () => {
            fetch(`/emails/${email.id}`, {
              method: "PUT",
              body: JSON.stringify({
                archived: true,
              }),
            }).then(() => {
              load_mailbox("inbox");
            });
          });
          element.append(archiveButton);
        }

        document.querySelector("#emails-view").append(element);
        element.classList.add("email-box");

        if (email.read) {
          element.style.backgroundColor = "gray";
        }
        element.addEventListener("click", () => {
          view_email(email.id);
        });
      });
    });
}

function send_email(event) {
  const recipents = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  event.preventDefault();
  if (
    document.querySelector("#compose-recipients").value === "" ||
    document.querySelector("#compose-subject").value === ""
  ) {
    alert("Please fill in all fields");
    return false;
  }
  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipents,
      subject: subject,
      body: body,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      console.log(result);
      load_mailbox("sent");
    });
}

function view_email(id) {
  fetch(`/emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      document.querySelector("#emails-view").style.display = "none";
      document.querySelector("#compose-view").style.display = "none";
      document.querySelector("#emails-detail-view").style.display = "block";

      document.querySelector("#emails-detail-view").innerHTML =
        `<div class="email">Sender: ` +
        email.sender +
        `</div>` +
        `<div class="email">Recipients: ` +
        email.recipients +
        `</div>` +
        `<div class="email">Subject: ` +
        email.subject +
        `</div>` +
        `<div class="email">Time: ` +
        email.timestamp +
        `</div>` +
        `<div class="email">` +
        email.body +
        `</div>`;

      if (!email.read) {
        fetch(`/emails/${email.id}`, {
          method: "PUT",
          body: JSON.stringify({
            read: true,
          }),
        });
      }

      const replyButton = document.createElement("button");
      replyButton.innerHTML = "Reply";
      replyButton.classList.add("btn-dark", "btn-sm", "btn-outline-dark");
      replyButton.style.color = "white";
      replyButton.addEventListener("click", () => {
        reply_email(email);
      });
      document.querySelector("#emails-detail-view").append(replyButton);

      const unarchiveButton = document.createElement("button");
      unarchiveButton.innerHTML = "Unarchive";
      unarchiveButton.classList.add("btn-dark", "btn-sm", "btn-outline-dark");
      unarchiveButton.style.color = "white";
      unarchiveButton.addEventListener("click", () => {
        fetch(`/emails/${email.id}`, {
          method: "PUT",
          body: JSON.stringify({
            archived: false,
          }),
        }).then(() => {
          load_mailbox("inbox");
        });
      });
      document.querySelector("#emails-detail-view").append(unarchiveButton);
    });
}

function reply_email(email) {
  compose_email();
  document.querySelector("#compose-recipients").value = email.sender;
  if (email.subject.slice(0, 4) === "Re: ") {
    document.querySelector("#compose-subject").value = `${email.subject} `;
  } else {
    document.querySelector("#compose-subject").value = `Re: ${email.subject} `;
  }
  document.querySelector(
    "#compose-body"
  ).value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}\n`;
}
