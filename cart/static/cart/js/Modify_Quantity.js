const parentForm = document.querySelector("form[id*='cart']");

const getPageSegment = function () {
  const currentUrl = window.location.href;
  const urlSegments = currentUrl.split("/");

  const pageSegment = urlSegments[urlSegments.length - 4];

  return pageSegment;
};

const getQuantityInput = function (targetElement) {
  const pageSegment = getPageSegment();

  if (pageSegment !== "cart") return document.querySelector("#id_quantity");
  else {
    closestTableRow = targetElement.closest("tr");
    return closestTableRow.querySelector("input[id*='quantity']");
  }
};

const changeQuantityInputValue = function (quantityElement, selectedOption) {
  const productDetailQuantity =
    +selectedOption.textContent.match(/[^-]+$/)?.[0];

  if (!productDetailQuantity) return;

  quantityElement.value = productDetailQuantity;
};

const onProductDetailChanged = function (e) {
  const productDetailId = e.target.value;
  const quantifyField = getQuantityInput(e.target);
  const selectedOption = e.target.querySelector(
    `option[value='${productDetailId}']`
  );
  changeQuantityInputValue(quantifyField, selectedOption);
};

modifyFormOnProductDetailChanged = function () {
  parentForm.addEventListener("change", onProductDetailChanged);
};

document.addEventListener("DOMContentLoaded", modifyFormOnProductDetailChanged);
