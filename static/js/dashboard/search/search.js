document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("search-icon").addEventListener("click", function () {
        console.log("Search icon clicked!");
        handleSearchProduct();
    });


});

function handleSearchProduct() {
    const query = document.getElementById("search-product").value.trim();

    $.ajax({
        url: "/main/search/",
        type: "GET",
        data: {
            'q': query
        },
        success: function (response) {
            var modalBody = document.getElementById('searchResults');
            modalBody.innerHTML = '';
            if (response.length > 0) {
                response.forEach(function (product) {
                    var productHtml = '<div class="row mb-3">';
                    productHtml += '<div class="col-md-4"><img src="' + product.images[0] + '" alt="' + product.product_name + '" class="img-fluid"></div>';
                    productHtml += '<div class="col-md-8">';
                    productHtml += '<h5>' + product.product_name + '</h5>';
                    productHtml += '<p>Price: ' + product.price + '</p>';
                    productHtml += '</div></div>';
                    modalBody.innerHTML += productHtml;
                });
                if (response.length > 4) {
                    modalBody.innerHTML += '<a href="#" class="btn btn-primary">View all results</a>';
                }
            } else {
                modalBody.innerHTML = '<p>No results found.</p>';
            }
            $('#searchModal').modal('show');
            $('.modal-backdrop').remove();
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });

    return false;
}