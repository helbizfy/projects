document.addEventListener('DOMContentLoaded', function () {


  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('form').onsubmit = sendEmail;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#email-details-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {


  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-details-view').style.display = 'none';


  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  showMailbox(mailbox)

}

function sendEmail() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
    .then(response => response.json())
    .then(result => {
      // Loads "sent" mailbox after sending
      load_mailbox('sent')
    });

  return false
}

function showMailbox(mailbox) {
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Print emails
      console.log(emails)
      emails.forEach(email => {

        // Establishing variables
        const user = document.createElement('div')
        const subject = document.createElement('div')
        const timestamp = document.createElement('div')
        const sender = document.createElement('div')
        const archive = document.createElement('img')
        const mail = document.createElement('div')
        const read = document.createElement('div')
        mail.setAttribute('id', 'email')
        archive.setAttribute('src', 'static/mail/archive.svg')
        archive.setAttribute('id', 'archive')

        // Determine what to show based on mailbox ,assigning values to created elements


        if (mailbox === "sent") {
          user.innerHTML = `To: ${email.recipients}`
        } else {
          user.innerHTML = `From: ${email.sender}`
        }

        subject.innerHTML = email.subject
        timestamp.innerHTML = email.timestamp

        if (email.read === true) {
          read.classList.add('badge', 'badge-primary')
          read.style.width = '50px'
          read.innerHTML = 'Read'
        } else {
          read.classList.add('badge', 'badge-danger')
          read.innerHTML = 'Unread'
        }

        if (mailbox === "inbox" || mailbox === "archive") {
          mail.append(read, user, subject, timestamp, archive)
        } else {
          mail.append(user, subject, timestamp)
        }



        // Styling

        subject.classList.add('col-4')
        subject.style.font = '20px bold Arial, sans-serif'
        user.classList.add('col-4')
        timestamp.classList.add('col-3')
        mail.classList.add('d-flex', 'container', 'mb-2', 'border', 'border-light')
        mail.style.padding = '0'
        mail.style.background = '#F8F8F8'



        //Update #emails-view with email

        document.querySelector('#emails-view').append(mail)

        // Functions for "mark as read", "archive", "email details"


        archive.addEventListener('click', () => archiveMail(email))

        mail.addEventListener('click', () => emailDetails(email))

        mail.addEventListener('click', () => markEmailRead(email))


      })
    });

}


function archiveMail(email) {
  event.stopPropagation()
  console.log(email.archived)
  const archiveValue = !email.archived
  fetch(`/emails/${email["id"]}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: archiveValue
    })
  })
    .then(() => load_mailbox("inbox"));
}

function emailDetails(email) {

  // Get user logged in

  const user = document.getElementById("loggedUser").innerHTML

  // Hiding/Displaying blocks

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-details-view').style.display = 'block';
  document.querySelector('#email-details-view').innerHTML = ''

  // Creating necessary divs

  const recipient = document.createElement('div')
  const subject = document.createElement('div')
  const timestamp = document.createElement('div')
  const sender = document.createElement('div')
  const content = document.createElement('div')
  const button = document.createElement('button')
  const mail = document.createElement('div')

  // Disabling 'replay' button in 'sent' mailbox

  if (user === email.sender) {
    mail.append(subject, recipient, sender, timestamp, content)
  } else {
    mail.append(subject, recipient, sender, timestamp, content, button)
  }

  // Assigning values to created elements

  recipient.innerHTML = `To: <b>${email.recipients}</b>`
  subject.innerHTML = email.subject
  timestamp.innerHTML = `Timestamp: <b>${email.timestamp}</b> <hr>`
  sender.innerHTML = `From: <b>${email.sender}</b>`
  content.innerHTML = email.body
  button.innerHTML = "Replay"

  //Email-view styles

  subject.classList.add('h2')
  timestamp.classList.add('small')
  button.classList.add('btn', 'btn-primary')
  content.style.height = "150px"
  content.style.border = "1px solid #D3D3D3"
  content.style.borderRadius = '5px'
  content.style.padding = '10px'
  content.style.marginBottom = '15px'

  document.querySelector('#email-details-view').append(mail)

  // Function to replay on email

  button.addEventListener('click', () => emailReplay(email))

}

function markEmailRead(email) {
  console.log(email.read)
  fetch(`/emails/${email["id"]}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
}

function emailReplay(email) {
  console.log(`Re:${email.subject}`);
  compose_email()
  document.querySelector('#compose-recipients').value = email.sender;
  document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote: ${email.body}`
  if (email['subject'].includes('Re:')) {
    document.querySelector('#compose-subject').value = email.subject;
  } else {
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  }
}



