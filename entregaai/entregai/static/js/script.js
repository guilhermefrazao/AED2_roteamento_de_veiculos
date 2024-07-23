document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('algorithmForm');
    const mapContainer = document.getElementById('mapContainer');
    const mapFrame = document.getElementById('mapFrame');
    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');

    let mapUrls = [];
    let currentIndex = 0;

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        fetch('', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mapUrls = data.map_urls;
                currentIndex = 0;
                updateMap();
            } else {
                alert('Error generating map. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    prevButton.addEventListener('click', function() {
        if (mapUrls.length > 0) {
            currentIndex = (currentIndex - 1 + mapUrls.length) % mapUrls.length;
            updateMap();
        }
    });

    nextButton.addEventListener('click', function() {
        if (mapUrls.length > 0) {
            currentIndex = (currentIndex + 1) % mapUrls.length;
            updateMap();
        }
    });

    function updateMap() {
        mapFrame.src = mapUrls[currentIndex];
    }
});
