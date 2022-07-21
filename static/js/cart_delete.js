
deletebtns = document.getElementsByClassName('delete-cart')

for (let i = 0; i < deletebtns.length; i++) {
    deletebtns[i].addEventListener('click', function() {
        var roomid = this.dataset.room
        var action = this.dataset.action
        console.log('roomid:', roomid, 'action:', action)
        updateUserOrder(roomid, action)
    })
    
}


function updateUserOrder(roomid, action){
    console.log('sending data')


    var url = '/basket/delete/';

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
        console.log('data:', data)
        location.reload()
    })
} 