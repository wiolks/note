document.addEventListener('DOMContentLoaded', function() {
    // Функция для обновления скрытого поля перед отправкой формы
    window.updateContent = function() {
        const editorContent = document.getElementById('editor').innerHTML;
        document.getElementById('content').value = editorContent;
    }

    // Пример: Обработка списков дел (зачеркивание) - если контент содержит списки
    const noteContent = document.querySelector('.note-content');
    if (noteContent) {
        noteContent.addEventListener('click', function(event) {
            if (event.target.tagName === 'LI') {
                event.target.classList.toggle('completed');
            }
        });
    }
});