function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

var months = document.querySelectorAll(".months")
var prices = document.querySelectorAll(".final-price")
var resultPrice = document.querySelectorAll(".price-fs-10")

for (let i = 0; i < months.length; i++) {
  months[i].parentElement.onclick = function () {
    const month = parseInt(months[i].innerText)
    const j = Math.floor(i / 3)
    const price = parseInt(prices[j].innerText)
    const result = parseFloat((price / month).toFixed(2))
    resultPrice[j].innerText = result + " AZN"
  }
}

const leftButton = document.querySelector(".btn-left-new");
const rightButton = document.querySelector(".btn-right-new");
const leftChosenButton = document.querySelector(".btn-left-chosen");
const rightChosenButton = document.querySelector(".btn-right-chosen");
const furnitureItem = document.querySelector(".custom-card");
var furnitureGroupItem = document.querySelector(".custom-card-group");
var furnitureChosenItem = document.querySelector(".custom-chosen-card-group");
var allItems = document.querySelectorAll(".custom-card-group .custom-card");
var allChosenItems = document.querySelectorAll(".custom-chosen-card-group .custom-card");
var scrollAmount = 0;


function scrollCards() {
  if (scrollAmount == allItems.length - 5) {
    furnitureGroupItem.scrollBy({
      left: -furnitureGroupItem.clientWidth,
      behavior: "smooth",
    });
    scrollAmount = 0;
  }
  else {
    furnitureGroupItem.scrollBy({
      left: furnitureItem.clientWidth,
      behavior: "smooth",
    });
    scrollAmount += 1;
  }
}

if (furnitureGroupItem) {
  var scrollInterval = setInterval(scrollCards, 2000);
}

function scrollChosenCards() {
  if (scrollAmount == allChosenItems.length - 5) {
    furnitureChosenItem.scrollBy({
      left: -furnitureChosenItem.clientWidth,
      behavior: "smooth",
    });
    scrollAmount = 0;
  }
  else {
    furnitureChosenItem.scrollBy({
      left: furnitureItem.clientWidth,
      behavior: "smooth",
    });
    scrollAmount += 1;
  }
}

if (furnitureChosenItem) {
  var scrollChosenInterval = setInterval(scrollChosenCards, 2000);
}


if (leftButton) {
  leftButton.addEventListener("click", () => {
    if (furnitureGroupItem.scrollLeft == 0) {
      furnitureGroupItem.scrollBy({
        left: furnitureGroupItem.clientWidth,
        behavior: "smooth",
      });
      scrollAmount = allItems.length - 5;
    }
    else {
      furnitureGroupItem.scrollBy({
        left: -furnitureItem.clientWidth,
        behavior: "smooth",
      });
      scrollAmount -= 1;
    }
  });
}

if (rightButton) {
  rightButton.addEventListener("click", () => {
    if (scrollAmount == allItems.length - 5) {
      furnitureGroupItem.scrollBy({
        left: -furnitureGroupItem.clientWidth,
        behavior: "smooth",
      });
      scrollAmount = 0;
    }
    else {
      furnitureGroupItem.scrollBy({
        left: furnitureItem.clientWidth,
        behavior: "smooth",
      });
      scrollAmount += 1;
    }
  });
}

if (leftChosenButton) {
  leftChosenButton.addEventListener("click", () => {
    if (furnitureChosenItem.scrollLeft == 0) {
      furnitureChosenItem.scrollBy({
        left: furnitureChosenItem.clientWidth,
        behavior: "smooth",
      });
      scrollAmount = allChosenItems.length - 5;
    }
    else {
      furnitureChosenItem.scrollBy({
        left: -furnitureItem.clientWidth,
        behavior: "smooth",
      });
      scrollAmount -= 1;
    }
  });
}

if (rightChosenButton) {
  rightChosenButton.addEventListener("click", () => {
    if (scrollAmount == allChosenItems.length - 5) {
      furnitureChosenItem.scrollBy({
        left: -furnitureChosenItem.clientWidth,
        behavior: "smooth",
      });
      scrollAmount = 0;
    }
    else {
      furnitureChosenItem.scrollBy({
        left: furnitureItem.clientWidth,
        behavior: "smooth",
      });
      scrollAmount += 1;
    }
  });
}

var categories = document.querySelectorAll(".w-19")
for (let i = 0; i < categories.length; i++) {
  categories[i].onmouseover = function () {
    let child = categories[i].querySelector('.w-420');
    child.classList.remove('d-none');
  }
  categories[i].onmouseout = function () {
    let child = categories[i].querySelector('.w-420');
    child.classList.add('d-none');
  }
}


let buttonBasket = document.querySelectorAll(".addBasket")
buttonBasket.forEach(element => {
  element.addEventListener("click", function () {
    const quantity = 1;
    fetch(`${location.origin}/api/basket/`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({
        'product': element.id,
        'quantity': quantity
      })
    }).then(response => response.json()).then(data => {
      if (data.message['success']) {
        window.alert('Produkt səbətə uğurla əlavə olundu!')
      }
    })
  });
});

let buttonWishlist = document.querySelectorAll(".heart-icon")
buttonWishlist.forEach(element => {
  element.addEventListener("click", function () {
    fetch(`${location.origin}/api/wishlist/`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({
        'product': element.dataset['id']
      })
    }).then(response => response.json()).then(data => {
      if (data.success) {
        window.alert('Produkt bəyəndikləriniz siyahısına əlavə olundu!')
      }
    })
  })
})


const burger = document.querySelector(".burger");
const asideMenu = document.querySelector("#aside-menu");
const exit = document.querySelector(".aside-header__exit");

burger.addEventListener("click", () => {
  asideMenu.classList.add("show");
});

exit.addEventListener("click", () => {
  asideMenu.classList.remove("show");
});
