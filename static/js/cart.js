$(document).ready(function () {
    $('.minus').click(function () {
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) - 1;
        count = count < 1 ? 1 : count;
        $input.val(count);
        $input.change();
        return false;
    });
    $('.plus').click(function () {
        var $input = $(this).parent().find('input');
        $input.val(parseInt($input.val()) + 1);
        $input.change();
        return false;
    });
});


let quantity = document.querySelector('.quantity')

let downButton = document.querySelectorAll("#stepDown")
downButton.forEach(element => {
    element.addEventListener("click", function () {
        let ProductID = this.getAttribute('data-id');
        let salePrice = element.parentElement.parentElement.parentElement.querySelector(".row .second .price .sale_price");
        let lastPrice = parseFloat(element.parentElement.parentElement.parentElement.querySelector(".row .second .price .last_price").innerText);
        let differPrice = 0
        if (salePrice) {
            salePrice = parseFloat(salePrice.innerText)
            differPrice = parseFloat((salePrice - lastPrice).toFixed(2))
        }
        let qty = element.parentElement.querySelector('.quantity').value
        let total = document.querySelector("#total");
        let subtotal = document.querySelector("#subtotal");
        let sale = document.querySelector("#sale");
        let main_total = document.querySelector('#main_total')
        if (qty >= 1) {
            fetch(`${location.origin}/api/basket/`, {
                method: 'PATCH',
                headers: {
                    'Content-type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    'productDown': ProductID,
                })
            }).then(response => response.json()).then(data => {
                if (data.success) {
                    total.innerHTML = (parseFloat(total.innerText) - parseFloat(lastPrice)).toFixed(2) + " azn"
                    if (salePrice) {
                        subtotal.innerHTML = (parseFloat(subtotal.innerText) - parseFloat(salePrice)).toFixed(2) + " azn"
                    }
                    else {
                        subtotal.innerHTML = (parseFloat(subtotal.innerText) - parseFloat(lastPrice)).toFixed(2) + " azn"
                    }
                    sale.innerHTML = (parseFloat(sale.innerText) + parseFloat(differPrice)).toFixed(2) + " azn"
                    main_total.innerHTML = total.innerHTML
                }
            })
        }
        if (qty == 1) {
            down.setAttribute('disabled', '');
        }
    });
});

let upButton = document.querySelectorAll("#stepUp")
upButton.forEach(element => {
    element.addEventListener("click", function () {
        let ProductID = this.getAttribute('data-id');
        let salePrice = element.parentElement.parentElement.parentElement.querySelector(".row .second .price .sale_price");
        let lastPrice = parseFloat(element.parentElement.parentElement.parentElement.querySelector(".row .second .price .last_price").innerText);
        let differPrice = 0
        if (salePrice) {
            salePrice = parseFloat(salePrice.innerText)
            differPrice = parseFloat((salePrice - lastPrice).toFixed(2))
        }
        let down = element.parentElement.querySelector('#stepDown')
        let total = document.querySelector("#total");
        let subtotal = document.querySelector("#subtotal");
        let sale = document.querySelector("#sale");
        let main_total = document.querySelector('#main_total')
        down.removeAttribute('disabled')
        fetch(`${location.origin}/api/basket/`, {
            method: 'PATCH',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'productUp': ProductID,
            })
        }).then(response => response.json()).then(data => {
            if (data.success) {
                total.innerHTML = (parseFloat(total.innerText) + parseFloat(lastPrice)).toFixed(2) + " azn"
                if (salePrice) {
                    subtotal.innerHTML = (parseFloat(subtotal.innerText) + parseFloat(salePrice)).toFixed(2) + " azn"
                }
                else {
                    subtotal.innerHTML = (parseFloat(subtotal.innerText) + parseFloat(lastPrice)).toFixed(2) + " azn"
                }
                sale.innerHTML = (parseFloat(sale.innerText) - parseFloat(differPrice)).toFixed(2) + " azn"
                main_total.innerHTML = total.innerHTML
            }
        })
    });
});

let removeButton = document.querySelectorAll(".remove")
removeButton.forEach(element => {
    element.addEventListener("click", function () {
        let ProductID = this.getAttribute('data-id');
        let salePrice = element.parentElement.querySelector(".row .second .price .sale_price");
        let lastPrice = parseFloat(element.parentElement.querySelector(".row .second .price .last_price").innerText);
        let differPrice = 0
        if (salePrice) {
            salePrice = parseFloat(salePrice.innerText)
            differPrice = parseFloat((salePrice - lastPrice).toFixed(2))
        }
        let qtyItem = parseInt(element.parentElement.querySelector(".row .second .qty .quantity").value);
        let total = document.querySelector("#total");
        let subtotal = document.querySelector("#subtotal");
        let sale = document.querySelector("#sale");
        let main_total = document.querySelector('#main_total')
        fetch(`${location.origin}/api/basket/`, {
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
                total.innerHTML = (parseFloat(total.innerText) - parseFloat((qtyItem * lastPrice).toFixed(2))).toFixed(2) + " azn"
                if (salePrice) {
                    subtotal.innerHTML = (parseFloat(subtotal.innerText) - parseFloat((qtyItem * salePrice).toFixed(2))).toFixed(2) + " azn"
                }
                else {
                    subtotal.innerHTML = (parseFloat(subtotal.innerText) - parseFloat((qtyItem * lastPrice).toFixed(2))).toFixed(2) + " azn"
                }
                sale.innerHTML = (parseFloat(sale.innerText) + parseFloat((qtyItem * differPrice).toFixed(2))).toFixed(2) + " azn"
                main_total.innerHTML = total.innerHTML
            }
        })
    });
});
