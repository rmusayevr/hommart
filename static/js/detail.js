const selectingItems = document.querySelectorAll(".selecting_item");
const selectedItem = document.querySelector(".selected_item");

selectingItems.forEach((item) => {
  item.addEventListener("click", () => {
    selectingItems.forEach((item) => {
      item.classList.remove("selected");
    });
    console.log(item);

    item.classList.add("selected");

    const imgSrc = item.querySelector("img").src;
    selectedItem.innerHTML = `<img class="selected_img object-fit-md-contain" src="${imgSrc}" />`;
  });
});

var cashMonths = document.querySelectorAll(".cash-months")
var priceProduct = document.querySelector(".price")
var monthlyPrice = document.querySelector(".monthly-price")


for (let i = 0; i < cashMonths.length; i++) {
  cashMonths[i].onclick = function () {
    var lastActive = document.querySelector('.active-month')
    lastActive.classList.remove("active-month")
    cashMonths[i].classList.add("active-month")
    monthNumber = parseInt(cashMonths[i].innerText)
    productPrice = parseInt(priceProduct.innerText)
    monthlyPrice.innerText = parseInt((productPrice / monthNumber))

  }
}

let qty = document.querySelector("#count")


$(document).ready(function() {
	$('.minus').click(function () {
		var $input = $(this).parent().find('input');
		var count = parseInt($input.val()) - 1;
		count = count < 1 ? 1 : count;
		$input.change();
    qty.setAttribute('value', count)
		return false;
	});
	$('.plus').click(function () {
		var $input = $(this).parent().find('input');
		$input.change();
    qty.setAttribute('value', parseInt($input.val()) + 1)
		return false;
	});
});

var versions = document.querySelectorAll('.versions')

const versionFilter = {
  url: `${location.origin}/api/versions/`,
  filterProductVersion(versionID) {
    let url = this.url;
    if (versionID) {
      url += `?id=${versionID}`;
    }
    fetch(url).then(response => response.json()).then(data => {
      document.getElementById("images").innerHTML = ''
      document.getElementById("cover_image").innerHTML = ''
      for (let i in data) {
        for (let j in data[i]['image']) {
          if (versionID == data[i]['id'] && j == 0) {
            document.getElementById("cover_image").innerHTML =
              `
              <div class="selected_item rounded-2 bg-light" id="cover_image">
                <img class="selecting_img object-fit-md-contain" src="${data[i]['image'][j]['image']}" />
              </div>
            `
          }
          if (versionID == data[i]['id']) {
            document.getElementById("images").innerHTML +=
              `
              <div class="selecting_item">
                <img class="selecting_img" src="${data[i]['image'][j]['image']}" />
              </div>
            `
          }
          if (versionID == versions[j].getAttribute('data-id')) {
            versions[j].classList.remove('btn-type-default');
            versions[j].classList.add('btn-type-danger');
            history.pushState(null, 'Product Versions', `${location.origin}/products/${data[i]['product']['slug']}/${data[i]['slug']}/`);
            document.querySelector(".addToBasket").setAttribute("data-id", versionID)
            document.querySelector(".heart-detail").setAttribute("data-id", versionID)
            document.querySelector("#count").setAttribute('value', 1);
          }
          else {
            versions[j].classList.remove('btn-type-danger');
            versions[j].classList.add('btn-type-default');
          }
        }
      }
    })
  }
}

for (let i = 0; i < versions.length; i++) {
  versions[i].onclick = function () {
    const versionID = this.getAttribute('data-id');
    versionFilter.filterProductVersion(versionID);
  }
}

let detailBasket = document.querySelector(".addToBasket")
detailBasket.addEventListener("click", function () {
  const quantity = qty.value;
  fetch(`${location.origin}/api/basket/`, {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({
      'product': detailBasket.dataset['id'],
      'quantity': parseInt(quantity)
    })
  }).then(response => response.json()).then(data => {
    if (data.message['success']) {
      window.alert('Produkt səbətə uğurla əlavə olundu!')
    }
  })
});

let detailWishlist = document.querySelectorAll(".heart-detail")
detailWishlist.forEach(element => {
  element.addEventListener("click", function () {
    fetch(`${location.origin}/api/wishlist/`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
        'X-CSRFToken': csrftoken
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

