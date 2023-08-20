let removeButton = document.querySelectorAll(".remove")
removeButton.forEach(element => {
    element.addEventListener("click", function () {
        let ProductID = this.getAttribute('data-id');
        fetch(`${location.origin}/api/wishlist/`, {
            method: 'DELETE',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'product': ProductID
            })
        }).then(response => response.json()).then(data => {
            if (data.success) {
                element.parentElement.style.display = "none"
            }
        });
    });
})

let buttonWBasket = document.querySelectorAll(".addWBasket")
buttonWBasket.forEach(element => {
    element.addEventListener("click", function () {
        const quantity = 1;
        fetch(`${location.origin}/api/basket/`, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'product': element.dataset['id'],
                'quantity': quantity
            })
        }).then(response => response.json()).then(data => {
            if (data.message['success']) {
              window.alert('Produkt səbətə uğurla əlavə olundu!')
            }
          })
    });
});