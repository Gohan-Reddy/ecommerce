var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log('productId: ', productID,' action: ',action)

        console.log('User: ', user)
        if(user == 'AnonymousUser'){
            console.log('Not Logged in!')

        }
        else{
            updateUserOrder(productID,action)
            
        }
    })
    
}


function updateUserOrder(productID, action){
    console.log('User is logged in sending data...')
    var url = '/updateItem/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFTOKEN':csrftoken,
        },
        body:JSON.stringify({'productID':productID, 'action':action})

        
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data:',data)
        location.reload()
    })

}