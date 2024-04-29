const swiper = new Swiper('.card-container', {
    slidesPerView: 5,
    spaceBetween: 15,
    
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
      
    },
  });
  

const tabs = document.querySelectorAll('[data-target]'),
tabContents = document.querySelectorAll('[content]')
//   console.log('->',tabContents)

tabs.forEach((tab)=>{
    tab.addEventListener('click',()=>{
        const target = document.querySelector(tab.dataset.target)
        console.log('-->',target)
        tabContents.forEach((tabContent)=>{
            tabContent.classList.remove('active-tab')
        });
        target.classList.add('active-tab')

        tabs.forEach((tab)=>{
            tab.classList.remove('active-tab')
        });

        tab.classList.add('active-tab')
    })
})





// JavaScript to handle modal opening and setting movie ID
document.querySelectorAll('.add-review').forEach(function(element) {
    element.addEventListener('click', function(event) {
        var movieId = element.getAttribute('data-movie-id');
        document.getElementById('movieIdInput').value = movieId;

    });

    document.getElementById('submitReviewBtn').addEventListener('click', function(event) {
        // Prevent the default form submission
        event.preventDefault();

        // Get the movie ID from the hidden input field
        var movieId = document.getElementById('movieIdInput').value;

        // Create the review data object
        var reviewData = {
            // movie_id: movieId,
            review_content: document.getElementById('reviewContent').value,
            rating: document.getElementById('rating').value
        };

        // Make the fetch call
        fetch('/watch/' + movieId + '/review-create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Add any additional headers if required
            },
            body: JSON.stringify(reviewData)
        })
        .then(response => {
            if (response.ok) {
                // If the response is successful, do something (e.g., close the modal)
                // You can add your desired actions here
                console.log('Review submitted successfully');
                // Close the modal if needed
                $('#reviewModal').modal('hide');
            } else {
                // If the response is not successful, handle the error
                console.error('Review submission failed');
                // You can handle errors according to your application's requirements
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle any errors that occur during the fetch request
        });
      });
});



const searchInput = document.getElementById('searchInput');
const searchResultsContainer = document.getElementById('searchResults');

searchInput.addEventListener('input', () => {
    const inputValue = searchInput.value.trim();

    if (inputValue === '') {
        searchResultsContainer.innerHTML = '';
        searchResultsContainer.style.display = 'none'; // Hide search results if input is empty
        return;
    }

    fetch(`/watch/search/?q=${inputValue}`)
        .then(response => response.json())
        .then(data => {
            searchResultsContainer.innerHTML = '';
            console.log(data,'====>data')

            if (data.length > 0) {
                data.forEach(movie => {
                    const movieElement = document.createElement('div');
                    movieElement.classList.add('movie');
                    movieElement.innerHTML = `
                    <a href="/watch/single_movie/${movie.id}" class="single-movie-container-link">
                        <div class="searched-movie-container">
                            <div class="searched-movie-box">
                                <img src="${movie.image}" alt="${movie.title}">
                                <div class="searched-title-release-date-cast">
                                    <h5 class='searched-movie-title'>${movie.title}</h5>
                                    <h6 class='searched-movie-title'>${movie.release_date}</h6>
                                    <p>${movie.cast.join(', ')}</p>
                                </div>
                            </div>
                        </div>
                    </a>
                        
                    `;
                    searchResultsContainer.appendChild(movieElement);
                });
            } else {
                searchResultsContainer.innerHTML = '<p>No results found.</p>';
            }
            searchResultsContainer.style.display = 'block'; // Show search results
        })
        .catch(error => {
            console.error('Error fetching search results:', error);
            searchResultsContainer.innerHTML = '<p>Failed to fetch search results.</p>';
        });
});
