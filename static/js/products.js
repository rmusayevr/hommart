$(document).ready(function () {
    if ($('.subDropdown')[0]) {
        $('.subDropdown').click(function () {
            $(this).toggleClass('plus-icon');
            $(this).toggleClass('minus-icon');
            if ($(this).text() == '+') {
                $(this).text('-');
            } else {
                $(this).text('+');
            }
            $(this).parent().parent().find('.sub-categories').slideToggle();
        });
    }
});

const rangeInput = document.querySelectorAll(".w-25 .range-input input"),
    priceInput = document.querySelectorAll(".w-25 .price-input input"),
    range = document.querySelector(".w-25 .slider .progress");
let categoryInput = document.querySelectorAll(".w-25 .parent-category-field")
let childInput = document.querySelectorAll(".w-25 .child-category-field")
let brandInput = document.querySelectorAll(".w-25 .brand-field")

const selectedCategories = [];
const selectedBrands = [];
let priceGap = 1000;

var url = `${location.origin}/api/products/`;
let totalProducts = 0;
let currentPage;

priceInput.forEach(input => {
    input.addEventListener("input", e => {
        let minPrice = parseInt(priceInput[0].value),
            maxPrice = parseInt(priceInput[1].value);

        if ((maxPrice - minPrice >= priceGap) && maxPrice <= rangeInput[1].max) {
            range.style.left = ((minPrice / rangeInput[0].max) * 100) + "%";
            if (e.target.className === "input-min") {
                rangeInput[0].value = minPrice;
            } else {
                rangeInput[1].value = maxPrice;
                range.style.right = 100 - (maxPrice / rangeInput[1].max) * 100 + "%";
            }
        }
        applyFilters();
    });
});

rangeInput.forEach(input => {
    input.addEventListener("input", e => {
        let minVal = parseInt(rangeInput[0].value),
            maxVal = parseInt(rangeInput[1].value);

        if ((maxVal - minVal) < priceGap) {
            if (e.target.className === "range-min") {
                rangeInput[0].value = maxVal - priceGap
            } else {
                rangeInput[1].value = minVal + priceGap;
            }
        } else {
            priceInput[0].value = minVal;
            priceInput[1].value = maxVal;
            range.style.left = ((minVal / rangeInput[0].max) * 100) + "%";
            range.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
        }
        applyFilters()
    });
});

categoryInput.forEach(element => {
    element.addEventListener("change", function () {
        const subCategories = this.closest('.form-check').querySelector('.sub-categories');
        subCategories.style.display = this.checked ? 'block' : 'none';
        const childCheckboxes = subCategories.querySelectorAll('.child-category-field');
        childCheckboxes.forEach(childCheckbox => {
            childCheckbox.checked = this.checked;
            const categorySlug = childCheckbox.dataset.slug
            if (this.checked) {
                selectedCategories.push(categorySlug);
            } else {
                const index = selectedCategories.indexOf(categorySlug);
                if (index > -1) {
                    selectedCategories.splice(index, 1);
                }
            }
        });
        console.log(selectedCategories);
        applyFilters();
    });
});

childInput.forEach(element => {
    element.addEventListener("change", function () {
        const parentCheckbox = this.closest('.sub-categories').previousElementSibling.querySelector('.parent-category-field');
        const allChildCheckboxes = this.closest('.sub-categories').querySelectorAll('.child-category-field');
        const isChecked = Array.from(allChildCheckboxes).every(cb => cb.checked);
        parentCheckbox.checked = isChecked;
        const categorySlug = this.getAttribute('data-slug');
        if (this.checked) {
            selectedCategories.push(categorySlug);
        } else {
            const index = selectedCategories.indexOf(categorySlug);
            if (index > -1) {
                selectedCategories.splice(index, 1);
            }
        }
        applyFilters();
    });
});

brandInput.forEach(element => {
    element.addEventListener("change", function () {
        const slug = this.dataset.slug;
        const checked = this.checked;
        if (checked) {
            selectedBrands.push(slug);
        } else {
            const index = selectedBrands.indexOf(slug);
            if (index > -1) {
                selectedBrands.splice(index, 1);
            }
        }
        applyFilters();
    });
});

function applyFilters(currentPage = 1) {
    const minPrice = parseInt(priceInput[0].value);
    const maxPrice = parseInt(priceInput[1].value);
    const params = new URLSearchParams({
        child_category: selectedCategories.join(','),
        brand: selectedBrands.join(','),
        min_price: minPrice,
        max_price: maxPrice,
        page: currentPage
    });
    fetchData(url, params, currentPage)
}

function fetchData(url, params, currentPage) {
    fetch(`${url}?${params}`).then(response => response.json()).then(data => {
        totalProducts = data.count || 0;
        document.getElementById('product-list').innerHTML = ''
        for (let i in data['results']) {
            document.getElementById('product-list').innerHTML +=
                `
                <div class="col-md-3 col-6 p-0">
                    ${userIsAuthenticated ?
                    `<img src="../../static/images/icons/svg-full-heart.svg" class="heart-icon" data-id="${data['results'][i]['version']}" alt="Heart Icon">`
                    :
                    `<img src="../../static/images/icons/svg-full-heart.svg" onclick="window.open('/login/', '_self');" class="heart-icon" data-id="${data['results'][i]['version']}" alt="Heart Icon">`
                }
                    
                    <a class="w-100" href="${data['results'][i]['detail_url']}">
                        <img src="${data['results'][i]['image']}" class="card-img-top h-210" alt="...">
                    </a>
                    <div class="card-body">
                        <p class="card-text mb-2 seats">${data['results'][i]['category']['name']}</p>
                        <a href="${data['results'][i]['detail_url']}" class="card-title text-decoration-none d-block w-100 fw-bold mb-2">${data['results'][i]['name']}</a>
                        <p class="btn btn-outline-danger disabled rounded-1">Bank kartları</p>
                        <p class="btn btn-outline-primary disabled rounded-1">Şəhər daxilində pulsuz çatdırılma</p>
                        <p class="btn btn-outline-success disabled rounded-1"><img src="../../static/images/icons/svg-stock.svg" class="me-1" alt=""> Stokda var</p>
                        <div class="d-md-flex justify-content-between productPrice">
                            <div class="d-flex flex-column pt-3 price">
                                ${data['results'][i]['in_sale'] ?
                    `<div class="text-decoration-line-through past-price text-secondary ps-3">
                                        ${data['results'][i]['final_price']} AZN
                                    </div>`: ``
                }
                                <div class="ps-3 pt-1 fw-bold fullPrice">
                                    ${data['results'][i]['price']} AZN
                                </div>
                            </div>
                            <div class="d-flex flex-column bg-body-tertiary p-2 mb-2 me-1 rounded-2 productCredit">
                                <div class="d-flex justify-content-evenly">
                                    <div>
                                        <button type="button" class="btn btn-outline-secondary monthlyPayment border-0 p-1 fw-light">6 ay</button>
                                    </div>
                                    <div>
                                        <button type="button" class="btn btn-outline-secondary monthlyPayment border-0 p-1 fw-light">12 ay</button>
                                    </div>
                                    <div>
                                        <button type="button" class="btn btn-outline-secondary monthlyPayment border-0 p-1 fw-light">18 ay</button>
                                    </div>
                                </div>
                                <div class="resultPrice fw-bold fs-10">
                                    ${data['results'][i]['twelve_price'].toFixed(2)} AZN
                                </div>
                            </div>
                        </div>
                        ${userIsAuthenticated ?
                    `<button type="submit" class="addBasket w-100 px-5 py-2 border-0 rounded-1" id="${data['results'][i]['version']}">Səbətə at</button>`
                    :
                    `<button type="submit" onclick="window.open('/login/', '_self');" class="addBasket w-100 px-5 py-2 border-0 rounded-1" data-id="${data['results'][i]['version']}">Səbətə at</button>`
                }
                    </div>
                </div>
            `
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
        });

        const paginationElement = document.querySelector('.block-27 ul');
        paginationElement.innerHTML = '';
        const totalPages = Math.ceil(totalProducts / 8);
        if (currentPage > 1) {
            paginationElement.innerHTML += `<li><a id="prevButton" href=?page=${currentPage - 1}>&lt;</a></li>`;
        }

        for (let page = 1; page <= totalPages; page++) {
            if (page === currentPage) {
                paginationElement.innerHTML += `<li class="active"><span>${currentPage}</span></li>`;
            }
            else {
                paginationElement.innerHTML += `<li><a class="page_links" href="?page=${page}">${page}</a></li>`;
            }
        }
        if (currentPage < totalPages) {
            paginationElement.innerHTML += `<li><a id="nextButton" href="?page=${currentPage + 1}">&gt;</a></li>`;
        }
        let pageNumbers = document.querySelectorAll('.page_links')
        for (let i = 0; i < pageNumbers.length; i++) {
            pageNumbers[i].onclick = function () {
                applyFilters(parseInt(pageNumbers[i].innerText));
                return false;
            }
        }
        if (document.getElementById('prevButton')) {
            document.getElementById('prevButton').onclick = function () {
                applyFilters(currentPage - 1)
                return false;
            }
        }

        if (document.getElementById('nextButton')) {
            document.getElementById('nextButton').onclick = function () {
                applyFilters(currentPage + 1)
                return false;
            }
        }
    })
}

const filter = document.querySelector(".showFilters");
const filters = document.querySelector("#filter_menu");
const exit_filter = document.querySelectorAll(".exit_filter");

filter.addEventListener("click", () => {
    filters.classList.add("show");
    filters.classList.remove("d-none");
});

exit_filter.forEach(element => {
    element.addEventListener("click", () => {
        filters.classList.remove("show");
        filters.classList.add("d-none");
    })
});

