const rangeInputMobile = document.querySelectorAll("#filter_menu .range-input input"),
    priceInputMobile = document.querySelectorAll("#filter_menu .price-input input"),
    rangeMobile = document.querySelector("#filter_menu .slider .progress");
let categoryInputMobile = document.querySelectorAll("#filter_menu .parent-category-field")
let childInputMobile = document.querySelectorAll("#filter_menu .child-category-field")
let brandInputMobile = document.querySelectorAll("#filter_menu .brand-field")

const selectedCategoriesMobile = [];
const selectedBrandsMobile = [];
let priceGapMobile = 1000;


var urlMobile = `${location.origin}/api/products/`;
let totalProductsMobile = 0;
let currentPageMobile;

priceInputMobile.forEach(input => {
    input.addEventListener("input", e => {
        let minPrice = parseInt(priceInputMobile[0].value),
            maxPrice = parseInt(priceInputMobile[1].value);

        if ((maxPrice - minPrice >= priceGapMobile) && maxPrice <= rangeInputMobile[1].max) {
            rangeMobile.style.left = ((minPrice / rangeInputMobile[0].max) * 100) + "%";
            if (e.target.className === "input-min") {
                rangeInputMobile[0].value = minPrice;
            } else {
                rangeInputMobile[1].value = maxPrice;
                rangeMobile.style.right = 100 - (maxPrice / rangeInputMobile[1].max) * 100 + "%";
            }
        }
        applyFiltersMobile();
    });
});

rangeInputMobile.forEach(input => {
    input.addEventListener("input", e => {
        let minVal = parseInt(rangeInputMobile[0].value),
            maxVal = parseInt(rangeInputMobile[1].value);

        if ((maxVal - minVal) < priceGapMobile) {
            if (e.target.className === "range-min") {
                rangeInputMobile[0].value = maxVal - priceGapMobile
            } else {
                rangeInputMobile[1].value = minVal + priceGapMobile;
            }
        } else {
            priceInputMobile[0].value = minVal;
            priceInputMobile[1].value = maxVal;
            rangeMobile.style.left = ((minVal / rangeInputMobile[0].max) * 100) + "%";
            rangeMobile.style.right = 100 - (maxVal / rangeInputMobile[1].max) * 100 + "%";
        }
        applyFiltersMobile()
    });
});

categoryInputMobile.forEach(element => {
    element.addEventListener("change", function () {
        const subCategories = this.closest('.form-check').querySelector('.sub-categories');
        subCategories.style.display = this.checked ? 'block' : 'none';
        const childCheckboxes = subCategories.querySelectorAll('.child-category-field');
        childCheckboxes.forEach(childCheckbox => {
            childCheckbox.checked = this.checked;
            const categorySlug = childCheckbox.dataset.slug
            if (this.checked) {
                selectedCategoriesMobile.push(categorySlug);
            } else {
                const index = selectedCategoriesMobile.indexOf(categorySlug);
                if (index > -1) {
                    selectedCategoriesMobile.splice(index, 1);
                }
            }
        });
        applyFiltersMobile();
    });
});

childInputMobile.forEach(element => {
    element.addEventListener("change", function () {
        const parentCheckbox = this.closest('.sub-categories').previousElementSibling.querySelector('.parent-category-field');
        const allChildCheckboxes = this.closest('.sub-categories').querySelectorAll('.child-category-field');
        const isChecked = Array.from(allChildCheckboxes).every(cb => cb.checked);
        parentCheckbox.checked = isChecked;
        const categorySlug = this.getAttribute('data-slug');
        if (this.checked) {
            selectedCategoriesMobile.push(categorySlug);
        } else {
            const index = selectedCategoriesMobile.indexOf(categorySlug);
            if (index > -1) {
                selectedCategoriesMobile.splice(index, 1);
            }
        }
        applyFiltersMobile();
    });
});

brandInputMobile.forEach(element => {
    element.addEventListener("change", function () {
        const slug = this.dataset.slug;
        const checked = this.checked;
        if (checked) {
            selectedBrandsMobile.push(slug);
        } else {
            const index = selectedBrandsMobile.indexOf(slug);
            if (index > -1) {
                selectedBrandsMobile.splice(index, 1);
            }
        }
        applyFiltersMobile();
    });
});

function applyFiltersMobile(currentPageMobile = 1) {
    const minPrice = parseInt(priceInputMobile[0].value);
    const maxPrice = parseInt(priceInputMobile[1].value);
    const params = new URLSearchParams({
        child_category: selectedCategoriesMobile.join(','),
        brand: selectedBrandsMobile.join(','),
        min_price: minPrice,
        max_price: maxPrice,
        page: currentPageMobile
    });
    fetchData(urlMobile, params, currentPageMobile)
}

function fetchData(urlMobile, params, currentPageMobile) {
    fetch(`${urlMobile}?${params}`).then(response => response.json()).then(data => {
        totalProductsMobile = data.count || 0;
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
                        <div class="d-flex justify-content-between productPrice">
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
                    `<button type="submit" class="addBasket w-100 border-0 rounded-1" id="${data['results'][i]['version']}">Səbətə at</button>`
                    :
                    `<button type="submit" onclick="window.open('/login/', '_self');" class="addBasket w-100 border-0 rounded-1" data-id="${data['results'][i]['version']}">Səbətə at</button>`
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
        const totalPages = Math.ceil(totalProductsMobile / 8);
        if (currentPageMobile > 1) {
            paginationElement.innerHTML += `<li><a id="prevButton" href=?page=${currentPageMobile - 1}>&lt;</a></li>`;
        }

        for (let page = 1; page <= totalPages; page++) {
            if (page === currentPageMobile) {
                paginationElement.innerHTML += `<li class="active"><span>${currentPageMobile}</span></li>`;
            }
            else {
                paginationElement.innerHTML += `<li><a class="page_links" href="?page=${page}">${page}</a></li>`;
            }
        }
        if (currentPageMobile < totalPages) {
            paginationElement.innerHTML += `<li><a id="nextButton" href="?page=${currentPageMobile + 1}">&gt;</a></li>`;
        }
        let pageNumbers = document.querySelectorAll('.page_links')
        for (let i = 0; i < pageNumbers.length; i++) {
            pageNumbers[i].onclick = function () {
                applyFiltersMobile(parseInt(pageNumbers[i].innerText));
                return false;
            }
        }
        if (document.getElementById('prevButton')) {
            document.getElementById('prevButton').onclick = function () {
                applyFiltersMobile(currentPageMobile - 1)
                return false;
            }
        }

        if (document.getElementById('nextButton')) {
            document.getElementById('nextButton').onclick = function () {
                applyFiltersMobile(currentPageMobile + 1)
                return false;
            }
        }
    })
}

