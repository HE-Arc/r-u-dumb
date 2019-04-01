function search_quiz(csrf_token) {
    console.log("bite");

    $.ajax({
        url : "search_quiz", // the endpoint
        type : "POST", // http method
        data : { 
            search_text : $('#quizSearch').val(),
            csrfmiddlewaretoken: csrf_token,
        }, // data sent with the post request
        dataType: 'json',

        // handle a successful response
        success : function(json) {
            
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            try {
                let elem = document.getElementById("quizz-container");
                let html = '<div class="row">';
                for(var key in json) {
                    var value = json[key];
                    html += '<div class="col-md-4"><a href="/quiz/'+key+'/"><div class="card mb-4 shadow-sm">'
                    html+= '<img class="card-img-top" src='+value[1]+ ' alt="Card image cap">'
                    html+= '<title>Quizz_image</title><rect width="100%" height="100%" fill="#55595c" /><div class="card-body">'   
                    html+= '<p class="card-text">'+ value[0]+'</p>'      
                    html+= '</div></div></div>'           
                        
                }
                html+='</div>'
                elem.innerHTML = html;
            } catch(error) {
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
    
};
