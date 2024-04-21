"use strict";

const toTitleCase = (action) => action[0].toUpperCase() + action.slice(1);

const getCSRFToken = function () {
  const cookie = document.cookie;
  const csrfToken = cookie.replace("csrftoken=", "");
  if (!csrfToken) throw Error("There's no CSRF Token in your COOKIE");
  return csrfToken;
};

const sendPostToBackEnd = async function ({ url, body }) {
  const csrfToken = getCSRFToken();
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": `${csrfToken}`,
    },
    body: JSON.stringify(body),
  });

  if (response.status != 200) throw Error();
  return response;
};

const updateDatabase = async function (
  data,
  { action = "update", quantity = 0 }
) {
  const productDetailId = data.dataset.productDetailId;
  try {
    if (action !== "delete" && action !== "update") return;

    await sendPostToBackEnd({
      url: "/cart/submit_data",
      body: {
        productDetailId,
        action,
        quantity,
      },
    });

    console.log(`${toTitleCase(action)} request sent successfully`);
  } catch (error) {
    console.error(`Error sending ${toTitleCase(action)} request:`);
  }
};

const changeQuantityWhenButtonClicked = function (clickedButton) {
  const productQuantityElement = clickedButton.closest(".product-quantity");
  const inputElement = productQuantityElement.querySelector(
    "input[aria-label='Quantity']"
  );

  const currentValue = parseInt(inputElement.value);

  const parentProductElement = clickedButton.closest(".product");

  if (clickedButton.classList.contains("btnPlus")) {
    inputElement.value = currentValue + 1;
  }

  if (clickedButton.classList.contains("btnMinus")) {
    inputElement.value = currentValue <= 0 ? 0 : currentValue - 1;
    if (+inputElement.value === 0) {
      deleteProduct(clickedButton);
      return;
    }
  }

  updateDatabase(parentProductElement, { quantity: inputElement.value });
};

const onQuantityChanged = function (changedElement) {
  if (changedElement?.tagName?.toLowerCase() === "button")
    changeQuantityWhenButtonClicked(changedElement);
  else if (
    changedElement instanceof Event &&
    changedElement?.target.ariaLabel === "Quantity"
  )
    changeQuantityWhenButtonClicked(changedElement.target);

  initializeTotalProductPrice();
};

const deleteProduct = function (clickedButton) {
  const parentProductElement = clickedButton.closest(".product");
  const nextElement = parentProductElement.nextElementSibling;
  if (nextElement.tagName.toLowerCase() === "hr") nextElement.remove();
  parentProductElement.remove();
  updateDatabase(parentProductElement, { action: "delete" });

  initializeTotalProductPrice();
};

const buttonTrigger = function (e) {
  const clickedButton = e.target.closest("button");
  if (!clickedButton) return;
  if (
    clickedButton.classList.contains("btnPlus") ||
    clickedButton.classList.contains("btnMinus")
  )
    return onQuantityChanged(clickedButton);

  if (clickedButton.classList.contains("btn-delete-from-cart"))
    return deleteProduct(clickedButton);
};

const addButtonDelegateEvent = function () {
  const productsElement = document.querySelector(".products");
  const btnSubmitPayElement = document.querySelector(".btn-submit-pay");
  productsElement.addEventListener("click", buttonTrigger);
  productsElement.addEventListener("change", onQuantityChanged);
  btnSubmitPayElement.addEventListener("", submitButtonClicked);
};

document.addEventListener("DOMContentLoaded", addButtonDelegateEvent);
