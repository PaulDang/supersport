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
            var searchInput = document.getElementById('search-product');
            var searchModal = document.getElementById('searchModal');

            modalBody.innerHTML = '';

            if (response.length > 0) {
                var ul = document.createElement('ul');
                ul.classList.add('list-group');

                var productsToShow = Math.min(response.length, 4);
                for (var i = 0; i < productsToShow; i++) {
                    var product = response[i];

                    var li = document.createElement('li');
                    li.classList.add('list-group-item', 'mb-3');

                    var productHtml = '<a href="/main/product/' + product.slug + '" class="d-flex align-items-center">';
                    productHtml += '<img src="' + product.images[0] + '" alt="' + product.product_name + '" style="width: 50px; height: 50px; margin-right: 10px;">';
                    productHtml += '<div>';
                    productHtml += '<p class="fw-bold mb-1">' + product.product_name + '</p>';
                    productHtml += '<p>Price: ' + product.price + '</p>';
                    productHtml += '</div>';
                    productHtml += '</a>';

                    li.innerHTML = productHtml;
                    ul.appendChild(li);
                }

                modalBody.appendChild(ul);

                if (response.length > 4) {
                    modalBody.innerHTML += '<div class="text-center mt-3"><a href="#" class="btn btn-primary">Xem tất cả kết quả &rarr;</a></div>';
                }
            } else {
                modalBody.innerHTML = `<p class="text-center">Rất tiếc, hiện không có kết quả phù hợp với từ khóa ${query} .</p>`;
            }

            const rect = searchInput.getBoundingClientRect();
            searchModal.style.top = `${rect.bottom + window.scrollY}px`;
            searchModal.style.left = `${rect.left + window.scrollX - 95}px`;
            searchModal.style.width = `${rect.width}px`;
            searchModal.style.display = 'block';

            $('.modal-backdrop').remove();
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });

    return false;
}

// Close modal when clicking outside
document.addEventListener('click', function(event) {
    const searchModal = document.getElementById('searchModal');
    const searchInput = document.getElementById('search-product');

    if (!searchModal.contains(event.target) && !searchInput.contains(event.target)) {
        searchModal.style.display = 'none';
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const searchIcon = document.getElementById('search-icon');
    const searchInput = document.getElementById("search-product");

    searchIcon.addEventListener('click', function() {
        handleSearchProduct();
    });

    searchInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            handleSearchProduct();
        }
    });
});