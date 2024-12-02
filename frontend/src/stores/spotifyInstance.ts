import { SpotifyApi } from '@spotify/web-api-ts-sdk'

async function get_spotify() {
  return SpotifyApi.withUserAuthorization(
    '4ca9111b9ddc480b917d2d992e0c30b4',
    window.location.origin + '/account',
    ['user-library-read'],
  )
}

export default get_spotify
