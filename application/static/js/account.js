function refresh() {
    localStorage.removeItem('user_data')
    localStorage.removeItem('playlists')
    window.location.reload()
  }
  
  function clear_storage() {
    localStorage.clear()
    window.location.reload()
  }