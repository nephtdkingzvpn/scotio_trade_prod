

document.addEventListener('DOMContentLoaded', (event) => {


    // spinning button when clicked
    const myadminForm = document.querySelector('#myadmin_form');
    const myadminBtn = document.querySelector('#myadmin_btn');
    const spinner = document.querySelector('#myadmin_spinner');
    const btnText = document.querySelector('#myadmin_btn_text');

    myadminForm.addEventListener('submit', (e)=>{
        e.preventDefault();

        spinner.classList.remove('d-none');
        btnText.textContent = '';
        myadminBtn.style.backgroundColor = 'rgb(46, 18, 114)';
        myadminBtn.disabled = true;

        myadminForm.submit();
    })

})
