import axios, { AxiosError, type AxiosInstance } from 'axios'
import { toast } from 'vue-sonner'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

class Backend {
  public axios: AxiosInstance

  constructor() {
    this.axios = axios.create({
      baseURL: BACKEND_URL,
      timeout: 5000,
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'), // Utility function to extract CSRF token
      },
    })
  }

  public async get_track(track_id: string) {
    const result = await this.axios.get(`/deezer/track`, {
      params: {
        track_id,
      },
    })

    return result.data
  }
}

const backend_instance = new Backend()

const backend = axios.create({
  baseURL: BACKEND_URL,
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

interface ErrorResponse {
  error: string
}

interface Track {
  id: number
  title_short: string
  artist: {
    name: string
  }
  album: {
    title: string
    cover_small: string
  }
  duration: number
  artists: Array<{
    artist_id: number
    artist_name: string
  }>
  preview: string
  playing?: boolean | null | undefined
}

interface Playlist {
  picture_medium: string
  title: string
  description: string
}

function toast_error(error: AxiosError) {
  // The request was made and the server responded with a status code
  // that falls out of the range of 2xx
  if (error.response) {
    if (error.response.data) {
      const error_reponse = error.response.data as ErrorResponse

      toast.error(`Error: ${error_reponse.error}`)
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

export { backend, backend_instance, toast_error, type Track, type Playlist }
