function applyFilter() {
    const filterSelect = document.getElementById('filterSelect');
    const selectedFilter = filterSelect.value;

    fetch('/apply_filter', {
        method: 'POST',
        body: `filter=${selectedFilter}`,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => {
            if (response.ok) {
                document.getElementById('displayedImg').src = document.getElementById('displayedImg').src + '?' + new Date().getTime();
            } else {
                console.error('Error applying filter');
            }
        });
}

function saveImage() {
    fetch('/save_image', {
        method: 'POST',
    })
        .then(response => {
            if (response.ok) {
                response.blob().then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'processed_image.png';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                });
            } else {
                console.error('Error saving image');
            }
        });
}

document.getElementById('imageForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);

    fetch('/open_image', {
        method: 'POST',
        body: formData,
    })
        .then(response => {
            if (response.ok) {
                return response.text();
            } else {
                console.error('Error opening image');
            }
        })
        .then(responseText => {
            document.getElementById('displayedImg').src = responseText;
        });
});
