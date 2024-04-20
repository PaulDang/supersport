window.onload = function () {
    var sizeOptions = document.querySelectorAll('.size-option');
    sizeOptions.forEach(function (option) {
        option.addEventListener('click', function () {
            // Xóa lớp 'selected' từ tất cả các kích thước
            sizeOptions.forEach(function (opt) {
                opt.classList.remove('selected');
            });
            // Thêm lớp 'selected' cho kích thước được chọn
            option.classList.add('selected');
            // Lấy thông tin về kích thước đã chọn
            var selectedSize = option.dataset.size;
            console.log("Selected size: " + selectedSize);
        });
    });
};


$(document).ready(function () {
    $('.thumbnail').click(function () {
        var imageUrl = $(this).attr('src');
        $('.main-image img').attr('src', imageUrl);
        $('.thumbnail').removeClass('active');
        $(this).addClass('active');
    });
});

$(document).ready(function () {
    var numImages = $('.slick-carousel').children().length; // Số lượng hình ảnh
    if (numImages < 5) { // Nếu số lượng hình ảnh ít hơn 4
        $('.previous').hide(); // Ẩn nút previous
        $('.next').hide(); // Ẩn nút next
    }
});

$(document).ready(function () {
    $('.slick-carousel').slick({
        slidesToShow: 4, // Hiển thị tối đa 4 hình ảnh cùng một lúc
        slidesToScroll: 1, // Trượt mỗi lần một hình ảnh
        autoplay: false, // Tự động trượt
        autoplaySpeed: 2000, // Tốc độ tự động trượt (nếu autoplay: true)
        arrows: true, // Hiển thị mũi tên điều hướng
        dots: false, // Hiển thị các nút chuyển slide
        infinite: true, // Vòng lặp vô hạn
    });
});