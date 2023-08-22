import bot from './assets/bot.svg'
import user from './assets/user.svg'

// Access UI elements on screen
const form = document.querySelector('form')
const chatContainer = document.querySelector('#chat-container')

let loadInterval;

// Return a loading screen
function loader (element) {
  element.textContent = ''
  // Calls function at specified interval aka 300ms
  loadInterval = setInterval(() => {
    element.textContent += '.'
    // Reset when three dots
    if (element.textContent === '....') element.textContent = ''
  }, 300)
}

function typeText (element, text) {
  let index = 0

  let interval = setInterval(() => {
    // Create a keyboard typing effect
    if (index < text.length) {
      element.innerHTML += text.charAt(index);
      index++
    } else {
      clearInterval(interval)
    }
  }, 20)
}

function generateUniqueId () {
  const timestamp = Date.now()
  const num = Math.random()
  const hex_s = num.toString(16)
  
  return `id-${timestamp}-${hex_s}`
}

// Return a different look depending on who is texting
function chatStripe(isAi, value, uniqueId) {
  return (
      `
      <div class="wrapper ${isAi && 'ai'}">
          <div class="chat">
              <div class="profile">
                  <img 
                    src=${isAi ? bot : user} 
                    alt="${isAi ? 'bot' : 'user'}" 
                  />
              </div>
              <div class="message" id=${uniqueId}>${value}</div>
          </div>
      </div>
    `
  )
}

const handleSubmit = async (e) => {
  e.preventDefault();

  // Key-Value pairs from our form
  const data = new FormData(form)
  // For user
  chatContainer.innerHTML += chatStripe(false, data.get('prompt'))
  form.reset()

  // For AI
  const uid = generateUniqueId()
  chatContainer.innerHTML += chatStripe(true, ' ', uid)

  // Scroll Up
  chatContainer.scrollTop = chatContainer.scrollHeight;

  const messageDiv = document.getElementById(uid)
  loader(messageDiv)

  // Fetch data from server
  const response = await fetch('http://localhost:5000', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      prompt: data.get('prompt')
    })
  })
  clearInterval(loadInterval)
  messageDiv.innerHTML = ''

  if (response.ok){
    const data = await response.json();
    const parsedData = data.bot.trim();
    console.log(parsedData)
    typeText(messageDiv, parsedData)
  } else {
    const err = await response.text()
    messageDiv.innerHTML = 'SOMETHING WENT WRONG!'

    alert(err)
  }
}

form.addEventListener('submit', handleSubmit)
form.addEventListener('keyup', (e) => {
  if (e.keyCode === 13) handleSubmit(e)
})