const currentDate = new Date();
let currentMonth = currentDate.getMonth();
let currentYear = currentDate.getFullYear();
let startDate = null;
let endDate = null;

const calendarBody = document.getElementById('calendarBody');
const currentMonthElement = document.getElementById('currentMonth');
const selectedDatesElement = document.getElementById('selectedDates');

const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

prevBtn.addEventListener('click',()=>{
    currentMonth--;
    renderCalendar();
});
nextBtn.addEventListener('click',()=>{
    currentMonth++;
    renderCalendar();
});

function renderCalendar(){
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    const firstDayIndex = new Date(currentYear, currentMonth, 1).getDay();

    currentMonthElement.textContent = new Date(currentYear, currentMonth).toLocaleDateString('default',{month: 'long', year: 'numeric'});
    
    let days = '';
    
    for (let i = 1; i <= firstDayIndex; i++) {
        days += `<div class="calendar-day"></div>`;
    }

    for (let i = 1; i <= daysInMonth; i++) {
        const date = new Date(currentYear, currentMonth, i);
        const className = getDayClassName(date);
        days += `<div class="calendar-day ${className}" onclick="selectDate(${i})">${i}</div>`;
    }

    calendarBody.innerHTML = days;
}

function selectDate(day){
    const clickedDate = new Date(currentYear, currentMonth, day);
        if (!startDate || endDate){
            startDate = clickedDate;
            endDate = null;
        } else if (clickedDate < startDate){
            startDate = clickedDate;
        } else if (clickedDate > startDate){
            endDate = clickedDate;
        }

        renderCalendar();
        updateSelectedDates();
    }

    function updateSelectedDates(){
        if(startDate && endDate){
            selectedDatesElement.textContent = `Fechas seleccionadas: ${formatDate(startDate)} - ${formatDate(endDate)}`;
        } else if (startDate){
            selectedDatesElement.textContent = `Fechas seleccionadas: ${formatDate(startDate)}`;
        } else {
            selectedDatesElement.textContent = `Fechas seleccionadas:`;
        }
    }

    function getDayClassName(date){
        if (startDate && date.toDateString() === startDate.toDateString()){
            return 'selected';
        }
        if (endDate && date.toDateString() === endDate.toDateString()){
            return 'selected';
        }
        if (startDate && endDate && date > startDate && date < endDate){
            return 'range';
        }
        return '';
    }

    function formatDate(date){
        return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`;
    }

    renderCalendar();
    updateSelectedDates();