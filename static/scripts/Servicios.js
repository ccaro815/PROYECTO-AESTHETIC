let serviceContainer = document.querySelector('.service-preview');
let serviceBox = serviceContainer.querySelectorAll('.service');

document.querySelectorAll('.grid-container .grid_item').forEach(grid_item =>{
  grid_item.onclick = () =>{
    serviceContainer.style.display = 'flex';
    let name = grid_item.getAttribute('data-name');
    serviceBox.forEach(service =>{
      let target = service.getAttribute('data-target');
      if(name == target){
        service.classList.add('active');
      }
    });
  };
});

serviceBox.forEach(close =>{
  close.querySelector('.fa-times').onclick = () =>{
    close.classList.remove('active');
    serviceContainer.style.display = 'none';
  };
});