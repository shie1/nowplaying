function setSong(artist,song){
    $('#tracktitle').text(song)
    $('#trackartist').text(artist)
    return true
}

setSong("Please wait...", "LOADING")