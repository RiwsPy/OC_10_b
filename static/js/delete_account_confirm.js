var delete_text = document.getElementById('delete_text');
var delete_account_confirm = document.getElementById('delete_account_confirm');
var delete_account = document.getElementById('delete_account')

function show_confirm_message(){
    let request = new Request('/user/delete_account/', {
        method: 'GET',
        headers: new Headers(),
        })
    fetch(request)
    .then((resp) => resp.json())
    .then((data) => {
        delete_text.innerText = data.text
        delete_account.style['display'] = 'none';
        delete_account_confirm.style['display'] = 'block';
    })
    .catch((error) => {
        alert("Erreur : " + error)});
}
