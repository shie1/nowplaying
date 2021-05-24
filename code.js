function setSong(artist,song){
    $('#tracktitle').text(song)
    $('#trackartist').text(artist)
    return true
}

function setCover(url){
    $('img#trackart').attr('src', url)
    return true
}

setSong("Please wait...", "LOADING")
setCover("https://i.pinimg.com/originals/ad/be/5f/adbe5f762b5a61c1024223ccb260786d.png")