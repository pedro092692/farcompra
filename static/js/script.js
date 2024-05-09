window.onload = function() {
    window.onpageshow = function(event) {
        if (event.persisted || performance.getEntriesByType("navigation")[0].type === 'back_forward') {
            location.reload();
        }
    };
   }

    const search_input = document.getElementById('search');
    search_input.addEventListener('keyup', search);
    search_input.addEventListener('input', search);



    const socket = io({autoConnect: false});
    socket.connect();
    // Get ul
    const resultElement = document.getElementById('results');

    function search(){
        socket.emit('search_query', search_input.value, per_page=8);
    }

    document.addEventListener('click', function(event){
        const clickElement = event.target;
        search_input
        const div_suggest = document.getElementById('suggest-list');
        if (!search_input.contains(clickElement)){
            div_suggest.style.display = 'none';
        }else{
            socket.emit('search_query', search_input.value, per_page=8);
            socket.on('search_results', function(data){
                if(data.results.length > 0){
                div_suggest.style.display = 'block';
                }
            });
        }

    });



    socket.on('search_results', function(data){
        //show container
        const container = document.getElementById('suggest-list');
        if(data.results.length > 0){
            container.style.display = 'block';
        }else{
            container.style.display = 'none';
        }


        resultElement.innerHTML = '';

        data.results.forEach(function(product){
            //create li
            const listItem = document.createElement('li');
            listItem.classList.add('list-group-item', 'cursor-pointer', 'font-weight-bold', 'li-product-suggest');
            //create anchor
            const anchor = document.createElement('a');
            if(product.prices.length > 0){
                listItem.innerHTML = product.name;

                anchor.setAttribute('href', '/search?barcode='+product.barcode+'&product_name='+product.name+'&query='+search_input.value)
                // Append anchor to li, then li to resultElement
                listItem.appendChild(anchor);
                resultElement.appendChild(listItem);
               // Event delegation on resultElement
               resultElement.addEventListener('click', function(event) {});
           }
        });
        // Event delegation on resultElement
        resultElement.addEventListener('click', function(event) {
         if (event.target.classList.contains('li-product-suggest')) {
              // Navigate to the desired URL
              window.location.href = event.target.querySelector('a').href;
            }
        });
    });









