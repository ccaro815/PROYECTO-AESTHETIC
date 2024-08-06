let hideText_btn = document.getElementById('hideText_btn');
let gridItems = document.querySelectorAll('.grid-item');

hideText_btn.addEventListener('click', () => {
    if (hideText_btn.textContent === 'Ver Menos') {
        for (let i = gridItems.length -1; i >= gridItems.length -4; i--){
            gridItems[i].style.display = "none";
        }
        hideText_btn.textContent = 'Ver Mas';
    }
    else{
        gridItems.forEach(item => {
            item.style.display = 'block'; 
        });
        hideText_btn.textContent ='Ver Menos';
    }       
});