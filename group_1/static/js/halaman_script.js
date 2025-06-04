const movies = [
  {
    title: "Sean Man",
    genre: "Action, Sci-Fi",
    poster: "../static/image/seanman.jpg",
    showtimes: ["12:00", "15:00", "18:30"]
  },
  {
    title: "Chitato",
    genre: "Drama, Comedy",
    poster: "../static/image/seanman.jpg",
    showtimes: ["13:30", "16:00", "19:45"]
  },
  {
    title: "MikMan",
    genre: "Action, Adventure",
    poster: "https://via.placeholder.com/300x450?text=MikMan",
    showtimes: ["11:00", "14:00", "17:30"]
  }
];

function loadMovies() {
  const moviesContainer = document.querySelector(".movies");
  moviesContainer.innerHTML = "";

  movies.forEach(movie => {
    const card = document.createElement("div");
    card.className = "movie-card";
    card.innerHTML = `
      <img src="${movie.poster}" alt="${movie.title} Poster">
      <div class="movie-info">
        <h4>${movie.title}</h4>
        <p class="genre">Genre: ${movie.genre}</p>
        <p>Showtimes:</p>
        <div class="showtimes">
          ${movie.showtimes.map(time => `<span>${time}</span>`).join("")}
        </div>
        <button onclick="alert('You selected ${movie.title}')">Book Now</button>
      </div>
    `;
    moviesContainer.appendChild(card);
  });
}

document.addEventListener("DOMContentLoaded", loadMovies);
