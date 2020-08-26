document.addEventListener('DOMContentLoaded', () =>{

    document.querySelectorAll('.hearts').forEach((button) =>{
        button.addEventListener('click', () => {
            heartPost(button);
        })
    });

    function heartPost(button) {
        button.removeEventListener('click', heartPost);
        var heartIcon = getChildElement(button, 'far fa-heart');
        var heartedIcon = document.createElement('i');
        heartedIcon.className = 'fas fa-heart';
        button.replaceChild(heartedIcon, heartIcon);
        button.className = "hearted";
        button.addEventListener('click', () =>{
            unheartPost(button);
        });
        var hearts = getChildElement(button, 'heart-num').innerHTML;
        hearts++;
        getChildElement(button, 'heart-num').innerHTML = hearts;
        
        fetch(window.location.href, {
            method: 'PUT',
            body: JSON.stringify({
                type: 'heart',
                collection: getCollectionId()
            }),
            credentials: 'same-origin',
            headers: {
                'X-CSRFToken': getToken()
            }
        });
    }

    document.querySelectorAll('.hearted').forEach((button) => {
        button.addEventListener('click', () => {
            unheartPost(button)
        })
    })

    function unheartPost(button) {
        button.removeEventListener('click', unheartPost);
        var heartedIcon = getChildElement(button, 'fas fa-heart');
        var heartIcon = document.createElement('i');
        heartIcon.className = 'far fa-heart';
        button.replaceChild(heartIcon, heartedIcon);
        button.className = "hearts";
        button.addEventListener('click', () =>{
            heartPost(button);
        });
        var hearts = getChildElement(button, 'heart-num').innerHTML;
        hearts--;
        getChildElement(button, 'heart-num').innerHTML = hearts;
        
        fetch(window.location.href, {
            method: 'PUT',
            body: JSON.stringify({
                type: 'unheart',
                collection: getCollectionId()
            }),
            credentials: 'same-origin',
            headers: {
                'X-CSRFToken': getToken()
            }
        });
    }

    document.querySelectorAll('.remove').forEach((button) => {
        button.addEventListener('click', () => {
            var item = button.parentElement;
            var i_id = getChildElement(item, 'c-item-id').innerHTML;
            var c_id = getCollectionId();
            var body = item.parentElement;
            body.removeChild(item); // remove from dom

            // fetch shit
            fetch(window.location.href, {
                method: 'PUT',
                body: JSON.stringify({
                    type: 'remove_item',
                    from: 'collection',
                    delete_id: i_id,
                    collection: c_id
                }),
                credentials: 'same-origin',
                headers: {
                    'X-CSRFToken': getToken()
                }
            })
        })
    });

    var url = window.location.href;

    function getToken() {
        let tokenName = 'csrftoken'
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

    function getCollectionId(){
        var indexStart = url.indexOf("view_collection/") +16; // get index number of beginning of id
        var id = url.substring(indexStart);

        return id;
    }

    function getChildElement(parentNode, wantedClass) {
        const children = parentNode.childNodes;
        for (child in children) {
            if (children[child].className === wantedClass) {
                return children[child];
            }
        }
    };

    var edit = document.getElementById('edit-collect');
    edit.addEventListener('click', () =>{
        var c_id = getCollectionId();
        var originalContent = edit.parentElement;
        var body = originalContent.parentElement;

        /* change banner
        var change_img = document.createElement('button');
        change_img.innerHTML = "Change banner";
        change_img.addEventListener('click', () =>{

        });*/

        var currentTitle = getChildElement(body, 'view-collect-title');
        var titleInput = document.createElement('input');
        titleInput.value = currentTitle.innerHTML;
        titleInput.id = 'edit-title';
        titleInput.className = 'form-control'
        var titleLabel = document.createElement('label');
        titleLabel.innerHTML = 'Title';
        titleLabel.for = 'edit-title';
        var titleGroup = document.createElement('div');
        titleGroup.className = 'form-group';
        titleGroup.appendChild(titleLabel);
        titleGroup.appendChild(titleInput);

        var currentDscrpt = getChildElement(originalContent, 'view-collect-dscrpt');
        var editArea = document.createElement('textarea');
        editArea.id = 'edit-dscrpt'
        editArea.innerHTML = currentDscrpt.innerHTML;
        editArea.className = "form-control";
        editArea.rows = 8;
        var dscrptLabel = document.createElement('label');
        dscrptLabel.innerHTML = 'Description';
        dscrptLabel.for = 'edit-dscrpt';
        var dscrptGroup = document.createElement('div');
        dscrptGroup.className = 'form-group';
        dscrptGroup.appendChild(dscrptLabel);
        dscrptGroup.appendChild(editArea);

        var publicCheck = document.createElement('input');
        publicCheck.type = 'checkbox';
        publicCheck.className = 'form-check-input';
        publicCheck.id = 'notify-check';
        publicCheck.value = 'True';
        var currentStatus = getChildElement(originalContent, 'view-collect-status');
        if (currentStatus.innerHTML.includes("Public")){
            publicCheck.checked = true;
        }
        var checkLabel = document.createElement('label');
        checkLabel.innerHTML = 'Make collection public';
        checkLabel.for = 'notify-check'
        checkLabel.className = "form-check-label";
        var checkGroup = document.createElement('div');
        checkGroup.className = 'form-group form-check';
        checkGroup.appendChild(publicCheck);
        checkGroup.appendChild(checkLabel);

        var saveBtn = document.createElement('button');
        saveBtn.innerHTML = 'Save';
        saveBtn.addEventListener('click', () =>{
            currentTitle.innerHTML = titleInput.value;
            currentDscrpt.innerHTML = editArea.value;
            if (publicCheck.checked){
                currentStatus.innerHTML = 'Public Collection';
            }else{
                currentStatus.innerHTML = 'Private Collection';
            }

            body.replaceChild(originalContent, editable);

            fetch(window.location.href, {
                method: 'PUT',
                body: JSON.stringify({
                    type: 'edit_collection',
                    title: titleInput.value,
                    dscrpt: editArea.value, 
                    notify: publicCheck.checked,
                    collection: c_id
                }),
                credentials: 'same-origin',
                headers: {
                    'X-CSRFToken': getToken()
                }
            })
        })
        var cancelBtn = document.createElement('button'); // revert changes
        cancelBtn.innerHTML = 'Cancel'
        cancelBtn.addEventListener('click', () =>{
            body.replaceChild(originalContent, editable);
        })
        var deleteBtn = document.createElement('button');
        deleteBtn.innerHTML = 'Delete';
        deleteBtn.addEventListener('click', () =>{
            console.log('delete');
            fetch(window.location.href, {
                method: 'DELETE',
                redirect: 'follow',
                body: JSON.stringify({
                    type: 'del_collection',
                    collection: c_id
                }),
                credentials: 'same-origin',
                headers: {
                    'X-CSRFToken': getToken()
                }
            }).then(function() {
                window.location.replace('../my_collections');
            })
            // redirect to my collections
        })

        var editable = document.createElement('div');
        var editForm = document.createElement('form');
        editForm.appendChild(titleGroup);
        editForm.appendChild(dscrptGroup);
        editForm.appendChild(checkGroup);
        editForm.appendChild(saveBtn);
        editable.appendChild(editForm);
        editable.appendChild(cancelBtn);
        editable.appendChild(deleteBtn);
        

        body.replaceChild(editable, originalContent);
        /* next steps: actual editing functionality */
    })
});