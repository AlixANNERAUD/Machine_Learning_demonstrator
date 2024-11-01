function set_search() {
    let field = document.getElementById('search-field').value;

    let parameters = new URLSearchParams(window.location.search);

    if (field.value !== '') {
      parameters.set('search', field);
    } else {
      parameters.delete('search');
    }

    window.location.href = '?' + parameters.toString();
}

function set_page(page) {
    let parameters = new URLSearchParams(window.location.search);

    if (page !== 1) {
      parameters.set('page', page);
    } else {
      parameters.delete('page');
    }

    window.location.href = '?' + parameters.toString();
}