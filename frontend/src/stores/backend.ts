import axios, { AxiosError, type AxiosInstance } from 'axios'
import { toast } from 'vue-sonner'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

class Backend {
  private axios: AxiosInstance

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

  public async get_tracks(page: number = 0, search: string = ''): Promise<[Track[], number]> {
    const response = await this.axios.get(`/tracks`, {
      params: {
        page,
        search,
      },
    })

    return [response.data.tracks, response.data.total_pages]
  }

  public async get_track(track_id: string): Promise<Track> {
    const response = await this.axios.get(`/deezer/track`, {
      params: {
        track_id,
      },
    })

    return response.data
  }

  public async classify(track_id: string): Promise<number[]> {
    const response = await this.axios.get(`/classify`, {
      params: {
        track_id,
      },
      timeout: 20000,
    })

    return response.data['genres'] as number[]
  }

  public async get_genre(genre_id: number): Promise<Genre> {
    const response = await this.axios.get(`/deezer/genre`, {
      params: {
        genre_id,
      },
    })

    return response.data as Genre
  }

  public async get_playlist(playlist_id: string): Promise<Playlist> {
    const response = await this.axios.get(`/deezer/playlist`, {
      params: {
        playlist_id,
      },
    })

    return response.data as Playlist
  }

  public async get_queues(): Promise<[string[], string[]]> {
    const response = await this.axios.get(`/queues`)

    return [response.data.download_queue, response.data.embedding_queue]
  }

  public async scrape(playlist_id: string): Promise<void> {
    const response = await this.axios.post(`/scrape`, {
      playlist_id,
    })

    if (response.data.error) {
      throw new Error(response.data.error)
    }
  }

  public async get_UMAP(): Promise<PlotData> {
    const response = await this.axios.get(`/umap`, {
      timeout: 30000,
    })

    return response.data as PlotData
  }

  public async get_PCA(): Promise<PlotData> {
    const response = await this.axios.get(`/pca`, {
      timeout: 30000,
    })

    return response.data as PlotData
  }

  public async search_deezer(query: string): Promise<Track[]> {
    const response = await this.axios.get(`/deezer/search`, {
      params: {
        query,
      },
    })

    return response.data.data as Track[]
  }

  public async compose(track_id: string): Promise<string[]> {
    const response = await this.axios.get(`/compose`, {
      params: {
        track_id,
      },
      timeout: 30000,
    })

    return response.data.similar_tracks as string[]
  }
}

const backend_instance = new Backend()

function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null
  return null
}

interface PlotData {
  x: number[]
  y: number[]
  z: number[]
  labels: string[]
}

interface Genre {
  id: number
  name: string
  picture: string
  picture_small: string
  picture_medium: string
  picture_big: string
  picture_xl: string
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

export { backend_instance, toast_error, type Track, type Playlist, type Genre }
