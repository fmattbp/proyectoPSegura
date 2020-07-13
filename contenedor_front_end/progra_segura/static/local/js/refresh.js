$(document).ready(function(){
    setInterval(
        function(){
            $('#actualizar').load('/tabla/')
        },6000
    );
});
