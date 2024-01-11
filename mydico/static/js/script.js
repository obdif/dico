// let debounceTimer;

// document.getElementById('wordSearch').addEventListener('input', function() {
//     clearTimeout(debounceTimer);
    
//     debounceTimer = setTimeout(function() {
//         search();
//     }, 500); // Adjust the delay time (in milliseconds) as needed
// });

// function search() {
//     const wordSearch = document.getElementById('wordSearch').value;

//     // Make an AJAX request to your Django view for immediate results
//     // Update the 'url' with the correct endpoint in your Django app
//     fetch(`/search/?wordSearch=${wordSearch}`)
//         .then(response => response.text())
//         .then(data => {
//             document.getElementById('searchResults').innerHTML = data;
//         })
//         .catch(error => {
//             console.error('Error:', error);
//         });
// }