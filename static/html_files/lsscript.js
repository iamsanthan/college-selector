$(function() {

    $('#search').keyup(function() {
        alert("Handler for .keyup() called.");

        $.ajax({
            type: "GET",
            url: "/firstweb/search_status/",
            data: {
                'search_text': $('#search').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
    });
});

function searchSuccess(data, textStatus, jqXHR) {
    $('#search-results').html(data)
}