function like(id) {
    var like_btn = document.querySelector(`[data-id='like-btn-${id}']`);
    var like_cnt = document.querySelector(`[data-id="like-cnt-${id}"]`);

    if (like_btn.style.backgroundColor == 'white') {
        fetch('/like/' + id)
        .then(response => response.json())
        .then(post => {
            like_cnt.innerHTML = post.likes;
        });

        like_btn.style.backgroundColor = 'red';
    }
    else {
        fetch('/like/' + id)
        .then(response => response.json())
        .then(post => {
            like_cnt.innerHTML = post.likes;
        });
        
        like_btn.style.backgroundColor = 'white';
    }
    return false;
}

function edit(id) {
    var edit_btn = document.querySelector(`[data-id='edit-btn-${id}']`);
    var edit_form = document.querySelector(`[data-id='edit-form-${id}']`);
    var text = document.querySelector(`[data-id='text-${id}']`);

    text.style.display = 'none';
    edit_form.style.display = 'block';
    edit_form.innerHTML = text.innerHTML;

    edit_btn.addEventListener('click', () => {
        fetch('/edit/' + id, {
            method: 'PUT',
            body: JSON.stringify({
                content: edit_form.value
            })
        })
        .then(response => response.json())
        .then(post => {
            text.innerHTML = post.content;
            text.style.display = 'block';
            edit_form.style.display = 'none';
        });
    });
}

function followUser(id) {
    var follow_btn = document.querySelector(`[data-id='follow-btn-${id}']`);
    var follow_cnt = document.querySelector(`[data-id='follow-cnt-${id}']`);

    fetch('/follow/' + id, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(post => {
        follow_cnt.innerHTML = post.followers;
        if (follow_btn.innerHTML == 'Follow') {
            follow_btn.innerHTML = 'Unfollow';
        }
        else {
            follow_btn.innerHTML = 'Follow';
        }
    });
}