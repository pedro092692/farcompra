function show_product_info(li){

    const div_prices = document.querySelectorAll('[id=prices]');
    for (const div_price of div_prices){
        div_price.style.display = "none";
    }

    info_div = li.children[0];
    info_div.style.display = 'block';
}

  // Function to set a value in session storage
                                function setSessionStorage(key, value) {
                                    sessionStorage.setItem(key, value);
                                }

                                // Function to get a value from session storage
                                function getSessionStorage(key) {
                                    return sessionStorage.getItem(key);
                                }


