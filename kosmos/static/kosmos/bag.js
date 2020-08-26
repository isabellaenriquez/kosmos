document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.remove').forEach((button) => {
        button.addEventListener('click', () => {
            var item = button.parentElement;
            var i_id = getChildElement(item, 'b-item-id').innerHTML;
            var body = item.parentElement;
            body.removeChild(item); // remove from dom

            // fetch shit
            fetch(window.location.href, {
                method: 'PUT',
                body: JSON.stringify({
                    type: 'remove_item',
                    from: 'bag',
                    delete_id: i_id
                }),
                credentials: 'same-origin',
                headers: {
                    'X-CSRFToken': getToken()
                }
            })
        })
    });

    function getToken() {
        var tokenName = 'csrftoken'
        // no cookies
        if (!document.cookie) {
            return null;
        }

        const token = document.cookie.split(';')
            .map(c => c.trim())
            .filter(c => c.startsWith(tokenName + '='));

        // no cookie
        if (token.length === 0) {
            return null;
        }

        return decodeURIComponent(token[0].split('=')[1]);
    }

    function getChildElement(parentNode, wantedClass) {
        var children = parentNode.childNodes;
        for (child in children) {
            if (children[child].className === wantedClass) {
                return children[child];
            }
        }
    };

    document.querySelectorAll('.edit-item').forEach((button) => {
        button.addEventListener('click', () => {
            editItem(button);
        })
    });

    function editItem(button) {
        var item = button.parentElement;
        var i_id = getChildElement(item, 'b-item-id').innerHTML;
        var remove = getChildElement(item, 'remove');

        var details = getChildElement(item, 'item-details');
        var originalOpen = getChildElement(details, 'open-date').innerHTML;
        //originalOpen = new Date(originalOpen);
        originalOpen = moment(new Date(originalOpen));
        originalOpen = formatDate(originalOpen);
        var originalExpiry = getChildElement(details, 'expiry-date').innerHTML;
        //originalExpiry = new Date(originalExpiry);
        originalExpiry = moment(new Date(originalExpiry));
        originalExpiry = formatDate(originalExpiry);
        var originalNotify = getChildElement(details, 'notify').innerHTML; // whether to send notifications for product or not
        var originalNotes = getChildElement(details, 'item-notes').innerHTML;

        // creating new elements starting with open date
        var editBlock = document.createElement('div');
        editBlock.id = "edit-block";
        var newOpen = document.createElement('input');
        newOpen.type = "date";
        newOpen.id = "openDate";
        newOpen.class = "newOpen";
        newOpen.defaultValue = originalOpen;
        var openLabel = document.createElement('label');
        openLabel.innerHTML = "Date Opened";
        openLabel.for = "openDate";

        // expiry date
        var newExpiry = document.createElement('input');
        newExpiry.type = "date";
        newExpiry.id = "expiry";
        newExpiry.class = "newExpiry";
        newExpiry.defaultValue = originalExpiry;
        var expiryLabel = document.createElement('label');
        expiryLabel.innerHTML = "Expiry";
        expiryLabel.for = "expiry";

        newOpen.addEventListener('change', () =>{
            var selectedOpen = new Date(newOpen.value + 'T00:00');
            var nextDay = new Date(selectedOpen.getTime() + 86400000);
            console.log('next day: ' + nextDay);
            newExpiry.setAttribute("min", formatDate(nextDay)); // min date for expiry after setting opening date
        })

        // notifications
        var notifyCheck = document.createElement('input');
        notifyCheck.type = 'checkbox';
        notifyCheck.className = 'form-check-input';
        notifyCheck.id = 'notify-check';
        notifyCheck.class = 'notify-check'
        notifyCheck.value = 'True'; // for server communication
        notifyCheck.checked = (originalNotify == 'true');
        var checkLabel = document.createElement('label');
        checkLabel.innerHTML = 'Notify when expired';
        checkLabel.for = 'notify-check'
        checkLabel.className = "form-check-label";
        var checkGroup = document.createElement('div');
        checkGroup.className = 'form-group form-check';
        checkGroup.appendChild(notifyCheck);
        checkGroup.appendChild(checkLabel);

        // notes
        var editNotes = document.createElement('textarea');
        editNotes.rows = 3;
        editNotes.placeholder = 'Notes...';
        editNotes.innerHTML = originalNotes;
        editNotes.className = 'form-control';

        // add new elements to div
        editBlock.appendChild(openLabel);
        editBlock.appendChild(newOpen);
        editBlock.appendChild(expiryLabel);
        editBlock.appendChild(newExpiry);
        editBlock.appendChild(checkGroup);
        editBlock.appendChild(editNotes);

        // replace with editing bloxk
        item.replaceChild(editBlock, details);
        var save = document.createElement('button');
        save.innerHTML = "Save Changes";
        var cancel = document.createElement('button');
        cancel.innerHTML = 'Cancel';
        cancel.addEventListener('click', () =>{
            item.replaceChild(details, editBlock);
            item.replaceChild(button, save);
            item.replaceChild(remove, cancel);
        })
        save.addEventListener('click', () => {
            //saveChanges(details, editBlock, item, button);
            //set new dates
            var saveOpen = getChildElement(details, 'open-date');
            saveOpen.innerHTML = newOpen.value;
            var saveExpiry = getChildElement(details, 'expiry-date');
            saveExpiry.innerHTML = newExpiry.value;

            //set notifications
            var newNotify = notifyCheck.checked;
            if (newNotify) {
                getChildElement(details, 'bag-item-status').innerHTML = 'KOSMOS will notify you when this expires.';
            } else {
                getChildElement(details, 'bag-item-status').innerHTML = 'KOSMOS will not notify you when this expires.';
            }

            // set notes
            getChildElement(details, 'item-notes').innerHTML = editNotes.value;
            item.replaceChild(details, editBlock);
            item.replaceChild(button, save);
            item.replaceChild(remove, cancel);

            // send changes to server
            fetch(window.location.href, {
                method: 'PUT',
                body: JSON.stringify({
                    type: 'edit_bag_item',
                    open: newOpen.value,
                    expiry: newExpiry.value,
                    notify: newNotify,
                    notes: editNotes.value,
                    item: i_id
                }),
                credentials: 'same-origin',
                headers: {
                    'X-CSRFToken': getToken()
                }
            })
        });
        item.replaceChild(save, button);
        item.replaceChild(cancel, remove);
    }

    function formatDate(date) {
        var d = new Date(date);
        var year = d.getFullYear();
        var month = d.getMonth() + 1;
        var day = d.getDate();
        if (month < 10) {
            month = '0' + month;
        }
        if (day < 10) {
            day = '0' + day;
        }

        var newDate = year + '-' + month + '-' + day;
        return newDate;
    }

});