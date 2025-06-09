document.addEventListener('DOMContentLoaded', () => {
  const currentPage = window.location.pathname;

  if (currentPage.includes('confirm')) {
    // HALAMAN KONFIRMASI
    const urlParams = new URLSearchParams(window.location.search);
    const film = urlParams.get('film');
    const jadwal = urlParams.get('jadwal');
    const jumlah = parseInt(urlParams.get('jumlah')) || 0;
    const harga = 50000;
    const total = harga * jumlah;

    // Tampilkan data di halaman
    document.getElementById('film').textContent = `${film} (Rp.50.000,00)`;
    document.getElementById('jadwal').textContent = jadwal;
    document.getElementById('jumlah').textContent = jumlah;
    document.getElementById('harga').textContent = `Rp.50.000,00`;
    document.getElementById('total').textContent = `Rp.${total.toLocaleString('id-ID')},00`;

    // Isi hidden form
    document.getElementById('inputFilm').value = film;
    document.getElementById('inputJadwal').value = jadwal;
    document.getElementById('inputJumlah').value = jumlah;
    document.getElementById('inputHarga').value = harga;

    // Tombol kembali
    document.getElementById('backBtn').addEventListener('click', () => {
      window.location.href = `/${film.toLowerCase()}`;
    });

  } else {
    // HALAMAN FILM
    const beliBtn = document.getElementById('beliBtn');
    if (beliBtn) {
      beliBtn.addEventListener('click', () => {
        const filmName = document.getElementById('judulFilm').textContent.trim();
        const jadwal = document.getElementById('jadwal').value;
        const jumlah = document.getElementById('jumlah').value;

        if (!jadwal || !jumlah || jumlah <= 0) {
          alert('HARAP MEMILIH JUMLAH KURSI.');
          return;
        }

        const url = `/confirm?film=${encodeURIComponent(filmName)}&jadwal=${encodeURIComponent(jadwal)}&jumlah=${jumlah}`;
        window.location.href = url;
      });
    }
  }
});
