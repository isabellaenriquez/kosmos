document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.remove-notif').forEach((button) => {
        button.addEventListener('click', () => {
            console.log('hello')
            let notification = button.parentElement
            let i_id = getChildElement(notification, 'item-id').innerHTML;
            let body = notification.parentElement;
            body.removeChild(notification); // remove notification from DOM

            let notifCount = document.getElementById('notif-count').innerHTML;
            notifCount -= 1;
            document.getElementById('notif-count').innerHTML = notifCount;

            fetch(window.location.href, {
                method: 'PUT',
                body: JSON.stringify({
                    type: 'remove_item',
                    from: 'bag',
                    notif: true,
                    delete_id: i_id
                }),
                credentials: 'same-origin',
                headers: {
                    'X-CSRFToken': getToken()
                }
            })
        });
    });
    function getToken() {
        const tokenName = 'csrftoken'
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
        const children = parentNode.childNodes;
        for (child in children) {
            if (children[child].className === wantedClass) {
                return children[child];
            }
        }
    };
});
