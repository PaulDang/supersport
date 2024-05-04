function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const handleDeleteUser = function () {
  $('.btn-trash').click(function () {
    
    const row = $(this).closest('tr');
    const userId = row.data('user-id');

    $('.btn-yes').click(function () {
      const request = {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        data: {
          user_id: userId,
        },
      };

      fetch(`/delete_user/${userId}/`, request)
        .then(function (res) {
          if (res.status === 200) {
            row.remove();
            alertify.success('Xóa user thành công');
          }
        })
        .catch(() => alertify.error('Có lỗi xảy ra khi xóa user!'));
    });
  });
};

function handleSearchUser(){
  const query = document.getElementById("search-user").value

  localStorage.setItem("lastSearchQuery", query);

  const checkQuery = query ? `?q=${query}` : ""
  const baseUrl = window.location.origin;

  window.location.replace(baseUrl + "/dashboard/user/" + checkQuery)
  return false
}

// Clear localstorage
document.getElementById("reset-btn").addEventListener("click", handleResetSearch);
function handleResetSearch() {
  localStorage.removeItem("lastSearchQuery");
}

// Remove local when user access others page
window.addEventListener("beforeunload", function() {
  const currentUrl = window.location.href;
  const baseUrl = window.location.origin + "/dashboard/user/";
  if (currentUrl !== baseUrl) {
    localStorage.removeItem("lastSearchQuery");
  }
});

// Replace text search on input tag when window onload
window.onload = function() {
  const lastSearchQuery = localStorage.getItem("lastSearchQuery");
  if (lastSearchQuery) {
    document.getElementById("search-user").value = lastSearchQuery;
  }
};

const handleUserTable = function () {
  handleDeleteUser();
};

document.addEventListener('DOMContentLoaded', handleUserTable);
