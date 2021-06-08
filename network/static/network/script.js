document.addEventListener('DOMContentLoaded', function () {
    //Loads first page of all posts
    allPosts(1)

});

function allPosts(page) {
    // If page 1, then 'previous' button does not show

    if (page == 1) {
        document.querySelector('#previous').style.display = 'none'
    } else {
        document.querySelector('#previous').style.display = 'block'
        document.querySelector('#previous').onclick = function () {
            allPosts(page - 1)
        }
    }

    document.querySelector('#all-posts-view').innerHTML = ""

    fetch(`/postsPage/${page}`)
        .then(response => response.json())
        .then(posts => {

            // If page has more than 10 posts, then 'next' button does shows

            if (posts.length < 10) {
                document.querySelector('#nextPage').style.display = 'none'
            } else {
                document.querySelector('#nextPage').style.display = 'block'
                document.querySelector('#nextPage').onclick = function () {
                    allPosts(page + 1)
                }
            }
            // Showing posts and styling
            posts.forEach(post => {

                const loggedUser = document.querySelector('#user').innerHTML


                const author = document.createElement('h5')
                const body = document.createElement('div')
                const editBox = document.createElement('textarea')
                const save = document.createElement('button')
                const timestamp = document.createElement('div')
                const likeBox = document.createElement('div')
                const likes = document.createElement('div')
                const like_symbol = document.createElement('img')
                const edit = document.createElement('button')
                const block = document.createElement('div')


                editBox.style.display = 'none'
                save.style.display = 'none'

                //Check if logged user has liked the post

                if (post.liked_by.includes(loggedUser)) {
                    like_symbol.setAttribute('src', 'static/network/heart-fill.svg')
                } else {
                    like_symbol.setAttribute('src', 'static/network/heart.svg')
                }

                if (loggedUser === post.author) {
                    edit.style.display = 'block'
                } else {
                    edit.style.display = 'none'
                }

                //Edit post button. Onclick div swap

                edit.onclick = function () {
                    editBox.style.display = 'block'
                    edit.style.display = 'none'
                    body.style.display = 'none'
                    save.style.display = 'block'
                }



                //Assiging values

                author.innerHTML = post.author
                body.innerHTML = post.body
                timestamp.innerHTML = post.timestamp
                edit.innerHTML = 'Edit post'
                editBox.innerHTML = post.body
                save.innerHTML = 'Save Post'

                //Styling

                block.classList.add('container-fluid', 'col-4')
                timestamp.classList.add('small')
                block.style.padding = '5px'
                block.style.margin = '5px 0px 5px 5px'
                block.style.border = "1px solid #D3D3D3"
                edit.classList.add('btn-sm', 'btn-primary', 'small')
                save.classList.add('btn-sm', 'btn-secondary', 'small')
                likeBox.classList.add('container-fluid', 'd-flex')
                likeBox.style.padding = '0'

                //Likebox styling and values
                likes.innerHTML = post.liked_by.length

                likeBox.append(like_symbol, likes)

                block.append(author, timestamp, body, likeBox, editBox, edit, save)

                document.querySelector('#all-posts-view').append(block)

                likeBox.addEventListener('click', () => likePost(post.id))

                author.addEventListener('click', () => viewProfile(post.author_id))


                //Save edited post function

                save.onclick = function () {
                    fetch(`/posts/${post.id}`, {
                        method: 'POST',
                        body: JSON.stringify({
                            newValue: editBox.value,
                        })
                    }).then(() => allPosts(1))
                }



            })
        });
}

//Like post function

function likePost(post_id) {
    const loggedUserId = document.querySelector('#user_id').innerHTML
    fetch(`/newlike/${post_id}`, {
        method: 'POST'
    }).then(() => allPosts(1))

}

//View user profile function

function viewProfile(user_id) {
    document.querySelector('#view-user-profile').style.display = 'block';
    document.querySelector('#all-posts-view').style.display = 'none';
    document.querySelector('#fallowing').style.display = 'none';
    document.querySelector('#newpostBlock').style.display = 'none';
    document.querySelector('#pagination').style.display = 'none';
    document.querySelector('#view-user-profile').innerHTML = '';
    document.querySelector('#view-user-profile').classList.add('d-flex', 'flex-column')

    const header = document.createElement('div')
    const postsBox = document.createElement('div')
    const heading = document.createElement('h2')

    heading.innerHTML = "Posts:"
    document.querySelector('#view-user-profile').append(header, heading, postsBox)

    fetch(`/fallowers/${user_id}`)
        .then(response => response.json())
        .then(user => {

            const username = document.createElement('h3')
            const fallowing = document.createElement('div')
            const fallowers = document.createElement('div')
            const button = document.createElement('button')
            const userInfo = document.createElement('div')

            const loggedUser = document.querySelector('#user').innerHTML

            //Following and followers count

            fallowing.innerHTML = `Following <strong>${user.fallowing.length}</strong>`
            fallowers.innerHTML = `Fallowers <strong>${user.fallowers.length}</strong>`
            username.innerHTML = user.user

            //Follow / Unfollow btns

            if (user.fallowers.includes(loggedUser)) {
                button.innerHTML = "Unfollow"
                button.classList.add('btn', 'btn-danger')
            } else {
                button.innerHTML = "Follow"
                button.classList.add('btn', 'btn-success')
            }

            if (user.user === loggedUser) {
                button.style.display = 'none'
            } else {
                button.style.display = "block"
            }

            //Stying

            userInfo.classList.add('container', 'col-6', 'd-flex', 'justify-content-between', 'align-items-center')
            userInfo.style.margin = '5px 0px 0px 0px'
            userInfo.style.border = "1px solid #D3D3D3"
            userInfo.style.borderRadius = "25px"
            button.style.margin = '5px'


            userInfo.append(username, fallowing, fallowers, button)
            header.append(userInfo)
            button.addEventListener('click', () => fallowUser(user_id))
        })

    //Show user posts

    fetch(`/posts`)
        .then(response => response.json())
        .then(posts => {
            posts.forEach(post => {
                if (post.author_id === user_id) {
                    const content = document.createElement('div')
                    const body = document.createElement('h6')
                    const timestamp = document.createElement('div')


                    body.innerHTML = `'${post.body}'`
                    timestamp.innerHTML = post.timestamp


                    content.classList.add('container', 'col-6', 'd-flex', 'justify-content-between', 'align-items-center', 'border')
                    timestamp.classList.add('small')
                    content.style.margin = '5px 0px 0px 0px'


                    content.append(body, timestamp)
                    postsBox.append(content)

                }

            })
        });
}

//Follow user function

function fallowUser(user_id) {
    fetch(`/fallowers/${user_id}`, {
        method: 'POST'
    }).then(() => viewProfile(user_id))

    return false
}

//Following page view

function fallowingView(page) {
    document.querySelector('#fallowing').innerHTML = ''

    //Pagination

    if (page == 1) {
        document.querySelector('#previous').style.display = 'none'
    } else {
        document.querySelector('#previous').style.display = 'block'
        document.querySelector('#previous').onclick = function () {
            fallowingView(page - 1)
        }
    }
    fetch(`/following/${page}`)
        .then(response => response.json())
        .then(posts => {

            //Pagination

            if (posts.length < 5) {
                document.querySelector('#nextPage').style.display = 'none'
            } else {
                document.querySelector('#nextPage').style.display = 'block'
                document.querySelector('#nextPage').onclick = function () {
                    fallowingView(page + 1)
                }
            }

            posts.forEach(post => {


                const loggedUser = document.querySelector('#user').innerHTML
                const loggedUserId = document.querySelector('#user_id').innerHTML


                const author = document.createElement('h5')
                const body = document.createElement('div')
                const timestamp = document.createElement('div')
                const likeBox = document.createElement('div')
                const likes = document.createElement('div')
                const like_symbol = document.createElement('img')
                const block = document.createElement('div')

                if (post.liked_by.includes(loggedUser)) {
                    console.log(loggedUser)
                    like_symbol.setAttribute('src', 'static/network/heart-fill.svg')
                } else {
                    like_symbol.setAttribute('src', 'static/network/heart.svg')
                }

                author.innerHTML = post.author
                body.innerHTML = post.body
                timestamp.innerHTML = post.timestamp

                block.classList.add('container-fluid', 'col-4')
                timestamp.classList.add('small')
                block.style.padding = '5px'
                block.style.margin = '5px 0px 5px 5px'
                block.style.border = "1px solid #D3D3D3"
                likeBox.classList.add('container-fluid', 'd-flex')
                likeBox.style.padding = '0'


                likes.innerHTML = post.liked_by.length

                likeBox.append(like_symbol, likes)

                block.append(author, timestamp, body, likeBox)

                document.querySelector('#fallowing').append(block)

                likeBox.addEventListener('click', () => likePost(post.id))
                likeBox.addEventListener('click', () => fallowingView(loggedUserId))

                author.addEventListener('click', () => viewProfile(post.author_id))




            }
            )
        })


}
