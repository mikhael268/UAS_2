const step1 = document.querySelector(".step1"),
    step2 = document.querySelector(".step2"),
    step3 = document.querySelector(".step3"),
    emailAddress = document.getElementById("emailAddress"),
    verifyEmail = document.getElementById("verifyEmail"),
    inputs = document.querySelectorAll(".otp-group input"),
    nextButton = document.querySelector('.nextButton'),
    verifyButton = document.querySelector(".next_button"); // <- Ini sesuai tombol "Verify" di HTML kamu

window.addEventListener("load", () => {
    emailjs.init("VBI2S5EbHIb55SZTm"); // Public key kamu
    step2.style.display = "none";
    step3.style.display = "none";
    nextButton.classList.add("disable");
});

const validateEmail = (email) => {
    let re = /\S+@\S+\.\S+/;
    if (re.test(email)) {
        nextButton.classList.remove("disable");
    } else {
        nextButton.classList.add("disable");
    }
};


nextButton.addEventListener("click", () => {
    const email = emailAddress.value;
    const otp = 2626; 


    sessionStorage.setItem("otp", otp);
    sessionStorage.setItem("email", email);


    const templateParameter = {
        OTP: otp,
        email: email
    };

    const serviceID = 'service_1q8y3od';
    const templateID = 'template_xhhpnxr';

    emailjs.send(serviceID, templateID, templateParameter)
        .then((response) => {
            console.log("SUCCESS!", response.status, response.text);
            alert("OTP berhasil dikirim ke email!");
            step1.style.display = "none";
            step2.style.display = "block";
            verifyEmail.textContent = email;
        })
        .catch((error) => {
            console.error("FAILED...", error);
            alert("Gagal mengirim OTP. Coba lagi.");
        });
});


verifyButton.addEventListener("click", () => {
    const enteredOtp = Array.from(inputs).map(i => i.value).join("");
    const realOtp = sessionStorage.getItem("otp");

    if (enteredOtp === realOtp) {
        alert("OTP cocok! Akses berhasil.");
        step2.style.display = "none";
        step3.style.display = "block";
    } else {
        alert("OTP salah. Silakan coba lagi.");
    }
});
