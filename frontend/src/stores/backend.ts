import axios, { AxiosError } from 'axios'
import { toast } from 'vue-sonner'

const backend = axios.create({
  baseURL: 'http://localhost:8000/api/',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken'), // Utility function to extract CSRF token
  },
})

function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null
  return null
}

function toast_error(error: AxiosError) {
  // The request was made and the server responded with a status code
  // that falls out of the range of 2xx
  if (error.response) {
    if (error.response.data && error.response.data.error) {
      toast.error(`Error: ${error.response.data.error}`)
    } else {
      toast.error(`${error.response.statusText} (${error.response.status})`)
    }
  } else if (error.request) {
    // The request was made but no response was received
    // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
    // http.ClientRequest in node.js
    toast.error(`No response received from server : ${error.message.toLowerCase()}`)
  } else {
    // Something happened in setting up the request that triggered an Error
    toast.error(`Failed to send request to server : ${error.message.toLowerCase()}`)
  }
}

export { backend, toast_error }
