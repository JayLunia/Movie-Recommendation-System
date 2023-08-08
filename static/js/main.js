$(document).ready(function(){

  
    $('#recommend').on('click', function(){
        let movie=$('#search').val();
        if(movie=='-1')
            alert('Please select a movie');
        else
            window.location.href = `movie/${encodeURIComponent(movie)}`;
    })
});