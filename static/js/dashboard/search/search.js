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
                var productsToShow = Math.min(response.length, 4);
                for (var i = 0; i < productsToShow; i += 2) {
                    var product1 = response[i];
                    var product2 = response[i + 1];

                    var rowContainer = document.createElement('div');
                    rowContainer.classList.add('row', 'mb-3');

                    if (product1) {
                        var productHtml1 = '<div class="col-md-6">';
                        productHtml1 += '<a href="product/' + product1.slug + '"><img src="' + product1.images[0] + '" alt="' + product1.product_name + '" style="width: 50%; height: 50%;">';
                        productHtml1 += '<div class="d-flex flex-column h-100 justify-content-center">';
                        productHtml1 += '<p class="fw-bold">' + product1.product_name + '</p>';
                        productHtml1 += '<p >Price: ' + product1.price + '</p>';
                        productHtml1 += '</div>';
                        productHtml1 += '</a></div>';
                        rowContainer.innerHTML += productHtml1;
                    }

                    if (product2) {
                        var productHtml2 = '<div class="col-md-6">';
                        productHtml2 += '<a href="product/' + product2.slug + '"><img src="' + product2.images[0] + '" alt="' + product2.product_name + '" class="img-fluid"></a>';
                        productHtml2 += '<div class="d-flex flex-column h-100 justify-content-center">';
                        productHtml2 += '<h5 class="fw-bold text-center" style="max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">' + product2.product_name + '</h5>';
                        productHtml2 += '<p class="text-center" style="max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">Price: ' + product2.price + '</p>';
                        productHtml2 += '</div>';
                        productHtml2 += '</div>';
                        rowContainer.innerHTML += productHtml2;
                    }

                    modalBody.appendChild(rowContainer);
                }

                if (response.length > 4) {
                    modalBody.innerHTML += '<div class="text-center"><a href="#" class="btn btn-primary">Xem tất cả kết quả &rarr;</a></div>';
                }
            } else {
                modalBody.innerHTML = `<p class="text-center">Rất tiếc, hiện không có kết quả phù hợp với từ khóa ${query} .</p>`;
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
