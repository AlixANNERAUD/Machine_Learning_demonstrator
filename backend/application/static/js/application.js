document.addEventListener('DOMContentLoaded', content_loaded);

const error_modal = document.getElementById('error-modal');
const error_modal_content = document.getElementById('error-modal-content');
const menu_buttons = document.querySelectorAll('.menu-list li a');
const main_content = document.getElementById('main-content');

function content_loaded() {
    sessionStorage.clear();

    // Add event listener to the menu list
    menu_buttons.forEach(menu_list => {
        menu_list.addEventListener('click', menu_list_clicked);
    })

    // Load the first menu item
    menu_buttons[0].click();
}

function show_error_message(message) {
    error_modal.classList.add('is-active');
    error_modal_content.innerHTML = message;
}

function close_error_modal() {
    error_modal.classList.remove('is-active');
}

function menu_list_clicked(event) {

    let text = event.target.innerText.trim().toLowerCase();

    for (let i = 0; i < menu_buttons.length; i++) {
        menu_buttons[i].classList.remove('is-active');
    }

    event.target.classList.add('is-active');

    try {
        switch (text) {
            case "details":
                get_and_cache("/account").then(account => {
                    main_content.innerHTML = account;
                }).catch(error => {
                    show_error_message(error);
                });
                break;
            case "list":
                get_and_cache("/tracks").then(list => {
                    main_content.innerHTML = list;

                }).catch(error => {
                    show_error_message(error);
                });
                break;
            case "plot":
                get_and_cache("/umap").then(plot => {
                    main_content.innerHTML = plot;
                    execute_scripts(main_content);
                }).catch(error => {
                    show_error_message(error);
                });
                break;
            default:
                throw new Error('Invalid menu item');
        }
    }
    catch (error) {
        show_error_message(error);
    }
}

function execute_scripts(element) {
    const scripts = element.querySelectorAll('script');

    console.log(scripts);

    scripts.forEach(script => {
        const new_script = document.createElement('script');
        new_script.textContent = script.textContent;
        document.head.appendChild(new_script).parentNode.removeChild(new_script);
    });
}

async function get_and_cache(uri, parameters = null) {
    return fetch(uri, {
        cache: 'force-cache',
    }).then(response => {
        if (response.ok) {
            return response.text();
        }
        else {
            throw new Error('Error loading data');
        }
    });

}

function logout() {
    localStorage.clear();
    window.location.reload();
    document.cookie.clear();
    window.location.reload();
}