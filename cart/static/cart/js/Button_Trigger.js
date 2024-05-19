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
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": `${csrfToken}`,
      },
      body: JSON.stringify(body),
    });

     if (!response.ok && response.status == 422) {
      throw new Error(await response.text())
    }
    
    return response;
  } catch (error) {
    throw error;
  }

  // if (response.status != 200) throw Error(); 
};

const updateDatabase = async function (
  data,
  { action = "update", quantity = 0 }
) {
  const cartDetailId = data.dataset.cartDetailId;
  try {
    if (action !== "delete" && action !== "update") return;

    const response = await sendPostToBackEnd({
      url: "/cart/submit_data",
      body: {
        cartDetailId,
        action,
        quantity,
      },
    });   

    console.log(`${toTitleCase(action)} request sent successfully`);
    return response;
  } catch (error) {
    throw error;
  }
};

const isFloat = (value) => typeof value === "number" && !isNaN(value) && Number.isFinite(value) && value % 1 !== 0;

const changeQuantityWhenButtonClicked = async function (clickedButton) {
  const productQuantityElement = clickedButton.closest(".product-quantity");
  const inputElement = productQuantityElement.querySelector(
    "input[aria-label='Quantity']"
  );
  const btnPlus = productQuantityElement.querySelector(".btnPlus");

  let currentValue = parseInt(inputElement.value); 

  if (currentValue <= 0) {
    inputElement.value = 1;
    return;
  }

  if (isFloat(currentValue)) {
    inputElement.value = Math.trunc(currentValue);
    return;
  }

  const parentProductElement = clickedButton.closest(".product");     

  try {
    if (clickedButton.classList.contains("btnPlus")) {
      currentValue += 1;
    }

    if (clickedButton.classList.contains("btnMinus")) {
      currentValue = currentValue <= 0 ? 0 : currentValue - 1;
      if (currentValue === 0) {
        deleteProduct(clickedButton);
        return;
      }
      btnPlus.classList.remove("disabled");
    }
    
    const response = await updateDatabase(parentProductElement, { quantity: currentValue});
    inputElement.value = currentValue;
    return response;
  }catch(error) {
      const errorFromBE = JSON.parse(error.message);
      console.error(errorFromBE?.message);
      if (clickedButton.tagName.toLowerCase() == "input")
      inputElement.value = errorFromBE?.old_quantity;
      btnPlus.classList.add("disabled");
  }
};

const onQuantityChanged = async function (changedElement) {
  if (changedElement?.tagName?.toLowerCase() === "button")
    await changeQuantityWhenButtonClicked(changedElement);
  else if (
    changedElement instanceof Event &&
    changedElement?.target.ariaLabel === "Quantity"
  )
    await changeQuantityWhenButtonClicked(changedElement.target);

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

const formSubmitHandler = function(e) {
  e.preventDefault();
  const firstProduct = document.querySelector(".product");
  if (!firstProduct) {
    alertify.error("Không có sản phẩm trong giỏ hàng");
    return;
  }
  this.submit();
}

const addButtonDelegateEvent = function () {
  const productsElement = document.querySelector(".products");
  productsElement.addEventListener("click", buttonTrigger);
  productsElement.addEventListener("focusout", onQuantityChanged);
  const checkOutForm = document.querySelector("#check-out");
  checkOutForm?.addEventListener("submit", formSubmitHandler);
};

document.addEventListener("DOMContentLoaded", addButtonDelegateEvent);
