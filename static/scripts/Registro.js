document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    const successMessage = document.getElementById('successMessage');

    registerForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const formData = new FormData(registerForm);
        const formDataObj = {};
        formData.forEach((value, key) => (formDataObj[key] = value));

        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formDataObj)
            });

            if (response.ok) {
                const result = await response.json();
                if (result.success) {
                    registerForm.style.display = 'none';
                    successMessage.style.display = 'flex';
                } else {
                    alert(result.message || 'Hubo un error en el registro.');
                }
            } else {
                console.error('Error en la respuesta del servidor');
            }
        } catch (error) {
            console.error('Error en la solicitud:', error);
        }
    });
});



