emailjs.init('VBI2S5EbHIb55SZTm'); 
let generatedOTP = '';
let emailUsed = '';

function sendOTP() {
    const email = document.getElementById('email').value.trim();
    const status = document.getElementById('status');

    if (!email) {
        status.innerText = 'Email cannot be empty.';
        status.style.color = 'red';
        return;
    }

    generatedOTP = Math.floor(1000 + Math.random() * 9000).toString(); // OTP 4 digit
    emailUsed = email;

    const templateParams = {
        OTP: generatedOTP,
        email: email
    };

    emailjs.send('service_1q8y3od', 'template_xhhpnxr', templateParams)
        .then(() => {
            
            fetch('/store_reset_otp', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email, otp: generatedOTP })
            });

            
            document.querySelector('.step1').style.display = 'none';
            document.querySelector('.step2').style.display = 'block';
            document.getElementById('verifyEmail').innerText = email;
            status.style.color = 'green';
            status.innerText = 'OTP has been sent successfully!';
        })
        .catch(error => {
            console.error('EmailJS Error:', error);
            status.style.color = 'red';
            status.innerText = 'Failed to send OTP.';
        });
}

function resendOTP() {
    sendOTP();
}

function verifyOTP() {
    const status = document.getElementById('status');
    const inputs = document.querySelectorAll('.otp-group input');
    const enteredOTP = Array.from(inputs).map(input => input.value.trim()).join('');

    if (enteredOTP.length !== 4) {
        status.innerText = 'Please enter the 4-digit OTP.';
        status.style.color = 'red';
        return;
    }

    fetch('/verify_reset_otp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: emailUsed, otp: enteredOTP })
    })
    .then(res => res.json())
    .then(data => {
        if (data.valid) {
            status.style.color = 'green';
            status.innerText = 'OTP valid, directing to the password reset page...';

            
            sessionStorage.setItem('reset_email', emailUsed);

            setTimeout(() => {
                window.location.href = '/reset_form'; 
            }, 1500);
        } else {
            status.style.color = 'red';
            status.innerText = 'The OTP is incorrect.!';
        }
    })
    .catch(err => {
        console.error('OTP Verification Error:', err);
        status.style.color = 'red';
        status.innerText = 'An error occurred during verification..';
    });
}


document.addEventListener("DOMContentLoaded", () => {
    const otpInputs = document.querySelectorAll(".otp-group input");

    otpInputs.forEach((input, index) => {
        input.addEventListener("input", () => {
            if (input.value.length === 1 && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
        });

        input.addEventListener("keydown", (e) => {
            if (e.key === "Backspace" && input.value === "" && index > 0) {
                otpInputs[index - 1].focus();
            }
        });
    });
});
