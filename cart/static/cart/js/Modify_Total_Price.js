"use strict";

const formatToVND = function (price) {
  return price
    .toLocaleString("vi-VN", {
      style: "currency",
      currency: "VND",
    })
    .replace("₫", "VNĐ");
};

const calculateTotalProductPrice = function (acc, productPriceElement, idx) {
  const parentRow = productPriceElement.closest(".product");
  const totalProductPriceElement = parentRow.querySelector(
    ".product-total-price"
  );
  const productQuantityElement = parentRow.querySelector(
    ".product-quantity input"
  );

  const productPrice = parseFloat(
    productPriceElement.textContent.slice(0, -4).replaceAll(",", "")
  );

  const productQuantity = productQuantityElement.value;

  const totalPrice = productPrice * productQuantity;

  totalProductPriceElement.textContent = `${formatToVND(totalPrice)}`;

  return acc + totalPrice;
};

const initializeTotalProductPrice = function () {
  const productPrices = document.querySelectorAll(".product-price");
  const totalPrice = [...productPrices].reduce(calculateTotalProductPrice, 0);
  const formattedTotalPrice = formatToVND(totalPrice);
  const productSumPrice = document.querySelector(".products-sum-price");
  const productTotalPrice = document.querySelector(".products-total-price");
  productSumPrice.textContent = productTotalPrice.textContent =
    formattedTotalPrice;
};

document.addEventListener("DOMContentLoaded", initializeTotalProductPrice);
