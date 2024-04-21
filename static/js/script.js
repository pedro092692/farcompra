    const search_input = document.getElementById('search');
    search_input.addEventListener('keyup', search);
    search_input.addEventListener('change', search);
    const socket = io({autoConnect: false});

    function search(){
        socket.connect();
        socket.emit('search_query', search_input.value);
    }

    function create_th(label){
        const table_th = document.createElement('th')
        table_th.setAttribute('scope', 'col')
        table_th.classList.add('text-sm')
        table_th.innerHTML = label
        return table_th
    }

    function create_td(data){
        const table_td = document.createElement('td')
        table_td.setAttribute('scope', 'row')
        table_td.innerHTML = data
        return table_td

    }

    // Get ul
    const resultElement = document.getElementById('results');

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
            listItem.classList.add('list-group-item', 'cursor-pointer', 'li-product');
            //create anchor
            const anchor = document.createElement('a');
            anchor.innerHTML = product.name;
            anchor.setAttribute('href', '/search/'+product.name)
            // Append anchor to li, then li to resultElement
            listItem.appendChild(anchor);
            resultElement.appendChild(listItem);
           // Event delegation on resultElement
           resultElement.addEventListener('click', function(event) {});
        });
        // Event delegation on resultElement
        resultElement.addEventListener('click', function(event) {
         if (event.target.classList.contains('li-product')) { // Check for click on li
              // Navigate to the desired URL
              window.location.href = event.target.querySelector('a').href;
            }
        });
    });









