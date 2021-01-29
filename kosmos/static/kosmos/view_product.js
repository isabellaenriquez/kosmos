//import moment from 'moment';

document.addEventListener('DOMContentLoaded', () =>{
    var addBtn = document.getElementById('add-product')
    
    addBtn.addEventListener('click', () =>{
        // show form
        showForm(addBtn);
    });

    function showForm(button){
        button.innerHTML = 'Cancel';
        button.addEventListener('click', () =>{
            hideForm(button);
        })
        document.getElementById("add-product-form").style.display = 'block';
    }

    function hideForm(button){
        button.innerHTML = 'Add product +';
        button.addEventListener('click', () =>{
            showForm(button);
        })
        document.getElementById("add-product-form").style.display = 'none';
    }

    var selection = document.getElementById('selection')
    if (selection.value === 'bag'){
        document.getElementById('dates').style.display = 'block';
        document.getElementById('openDate').required = true;
    }else{
        document.getElementById('dates').style.display = 'none';
        document.getElementById('openDate').required = false;
    }
    selection.addEventListener('change', () =>{
        // show date pickers if user chooses to add product to bag
        if (selection.value === 'bag'){
            document.getElementById('dates').style.display = 'block';
        }else{ // collection is chosen
            document.getElementById('dates').style.display = 'none';
        }
    })

    var openDate = document.getElementById('openDate');
    var expiry = document.getElementById('expiry');
    var productExp = document.getElementById('suggested-expiry').innerHTML;

    openDate.addEventListener('change', () =>{
        var selectedOpen = new Date(openDate.value + 'T00:00');
        console.log('open date selected: ' + selectedOpen);
        var nextDay = new Date(selectedOpen.getTime() + 86400000);
        console.log('next day: ' + nextDay);
        expiry.setAttribute("min", formatDate(nextDay)); // min date for expiry after setting opening date

        // calculate expiry date after setting opening date
        var expiryEstimate = moment(selectedOpen);
        expiryEstimate.add(productExp, 'M');
        expiryEstimate = formatDate(expiryEstimate)
        console.log(expiryEstimate);
        expiry.value = expiryEstimate;
    });

    function formatDate(date){
        var d = new Date(date);
        var year = d.getFullYear();
        var month = d.getMonth() + 1;
        var day = d.getDate();
        if (month < 10){
            month = '0' + month;
        }
        if (day < 10){
            day = '0' + day;
        }

        var newDate = year + '-' + month + '-' + day;
        return newDate;
    }

});
