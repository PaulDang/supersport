"use strict";

const changeQuantityWhenButtonClicked = function (clickedButton) {
  const productQuantityElement = clickedButton.closest(".product-quantity");
  const inputElement = productQuantityElement.querySelector(
    "input[aria-label='Quantity']"
  );

  const currentValue = parseInt(inputElement.value);

  if (clickedButton.classList.contains("btnPlus"))
    inputElement.value = currentValue + 1;
  if (clickedButton.classList.contains("btnMinus"))
    inputElement.value = currentValue <= 0 ? 0 : currentValue - 1;
};

const onQuantityChanged = function (changedElement) {
  if (changedElement?.tagName?.toLowerCase() === "button")
    changeQuantityWhenButtonClicked(changedElement);

  initializeTotalProductPrice();
};

const deleteProduct = function (clickedButton) {
  const parentProductElement = clickedButton.closest(".product");
  const nextElement = parentProductElement.nextElementSibling;
  if (nextElement.tagName.toLowerCase() === "hr") nextElement.remove();
  parentProductElement.remove();

  initializeTotalProductPrice();
};

const buttonTrigger = function (e) {
  const clickedButton = e.target.closest("button");
  if (!clickedButton) return;
  if (
    clickedButton.classList.contains("btnPlus") ||
    clickedButton.classList.contains("btnMinus")
  )
    onQuantityChanged(clickedButton);

  if (clickedButton.classList.contains("btn-delete-from-cart"))
    deleteProduct(clickedButton);
};

const addButtonDelegateEvent = function () {
  const productsElement = document.querySelector(".products");
  productsElement.addEventListener("click", buttonTrigger);
  productsElement.addEventListener("change", onQuantityChanged);
};

document.addEventListener("DOMContentLoaded", addButtonDelegateEvent);
