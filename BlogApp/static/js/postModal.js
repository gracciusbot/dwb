
function openModal(post) {
    const postDetailContent = document.getElementById('post-detail-content');
    console.log('Post details:', post); // Verifique os dados do post para depuração

    postDetailContent.innerHTML = ''; // Limpar conteúdo anterior

    // Criar conteúdo HTML com base no modelo Instagram
    const postHtml = `
        <div class="container py-4">
            <div class="row">
                <!-- Coluna para Foto do Post -->
                <div class="col-md-4 d-flex justify-content-center">
                    <img src="${post.photo_post || 'default-post.png'}" alt="Post image" 
                        class="img-fluid rounded-post" style="width: 200px; height: 200px; object-fit: cover;">
                </div>

                <!-- Coluna para Informações do Post e Autor -->
                <div class="col-md-8 d-flex flex-column">
                    <!-- Informações do Autor e Post -->
                    <div class="d-flex align-items-center mb-3">
                        <div class="me-3">
                            <img src="${post.author_photo || 'default-profile.png'}" alt="${post.author}" 
                                class="rounded-circle profile-img" style="width: 50px; height: 50px;">
                        </div>
                        <div class="flex-grow-1">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <a href="/profile/${post.author}" class="text-primary fw-bold">${post.author}</a>
                                    <span class="text-muted"> - ${new Date(post.created_at).toLocaleDateString()}</span>
                                </div>
                                <button class="btn btn-outline-primary" id="follow-btn" 
                                    data-author="${post.author}" 
                                    ${post.is_following ? 'disabled' : ''}>
                                    ${post.is_following ? 'Following' : 'Follow'}
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Título e Hashtags do Post -->
                    <h4>${post.title}</h4>
                    <p class="text-secondary">${post.hashtags ? post.hashtags.join(' ') : ''}</p>

                    <!-- Comentários -->
                    <div class="mt-4">
                        <h5>Comments</h5>
                        <ul class="list-group" id="comments-list">
                            ${renderComments(post.comments, 3)} <!-- Exibe os primeiros 3 comentários -->
                        </ul>
                        ${post.comments.length > 3 ? `
                            <button class="btn btn-link" id="show-more-comments">Show more comments</button>
                        ` : ''}
                    </div>
                </div>
            </div>
        </div>
    `;

    postDetailContent.innerHTML = postHtml;

    // Inicializar o modal do Bootstrap
    const postDetailModal = new bootstrap.Modal(document.getElementById('postDetailModal'));
    postDetailModal.show();

    // Event listener para o botão de follow
    document.getElementById('follow-btn')?.addEventListener('click', () => {
        const author = post.author;
        // Lógica de follow (realizar chamada AJAX para seguir o autor)
        console.log(`Following ${author}`);
    });

    // Event listener para mostrar mais comentários
    if (post.comments.length > 3) {
        document.getElementById('show-more-comments')?.addEventListener('click', () => {
            const commentsList = document.getElementById('comments-list');
            commentsList.innerHTML = renderComments(post.comments, post.comments.length); // Exibe todos os comentários
            document.getElementById('show-more-comments').style.display = 'none'; // Esconde o botão de mostrar mais
        });
    }
}

// Função para renderizar comentários limitados
function renderComments(comments, limit) {
    return comments.slice(0, limit).map(comment => `
        <li class="list-group-item">
            <a href="/profile/${comment.author}" class="text-primary">${comment.author}</a>
            <p>${comment.content}</p>
        </li>
    `).join('');
}

// Função para carregar os detalhes do post via API
function loadPostDetails(postId) {
    fetch(`/post/${postId}/`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                console.error('Error from API:', data.error);
                alert('Error loading post details.');
                return;
            }
            openModal(data);
        })
        .catch(error => console.error('Error loading post details:', error));
}

document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.btn-primary');

    buttons.forEach(button => {
        button.addEventListener('click', (event) => {
            const postId = event.target.dataset.postId;
            if (postId) {
                loadPostDetails(postId);
            } else {
                console.error('Post ID not found.');
            }
        });
    });
});
