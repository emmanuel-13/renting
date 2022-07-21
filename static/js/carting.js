updatebtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updatebtns.length; i++) {
    updatebtns[i].addEventListener('click', function(e) {
        e.preventDefault();
        var roomid = this.dataset.room
        var action = this.dataset.action
        console.log('roomid:', roomid, 'action:', action)
        updateUserOrder(roomid, action)
    })
    
}


function updateUserOrder(roomid, action){
    console.log('sending data')


    var url = '/basket/add/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({
            'roomid': roomid, 'action': action,
        })
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) => {
        console.log(data.qty)
        const cartButton = document.getElementById('basket-qty2');
        cartButton.textContent = data.qty;

        let cartQantity = document.querySelector(".cart-quantity");
        let bookingLabel = document.getElementById("start__booking-mobile");
        let containsItem = document.querySelector(".cart-items");
        let noItem = document.querySelector(".no-cart-items");

        // console.log(cartQantity.innerText)
        // console.log(cartQantity.textContent)
        // console.log(cartQantity.innerHTML)

        if (cartQantity.textContent = 0 ) {
            noItem.style.display = "block";
            containsItem.style.display = "none";
            bookingLabel.innerText = "start booking";
        }
        
        if (cartQantity.textContent = 1) {
            noItem.style.display = "none";
            containsItem.style.display = "block" ;
            bookingLabel.innerText = "Continue booking";
        }
    })
} 


// function runCart() {
//     let containsItem = document.querySelector(".cart-items");
//     let noItem = document.querySelector(".no-cart-items");

//     containsItem.style.display = "block";
//     bookingLabel.innerText = "Continue booking";
// }


