const loginStep1 = document.querySelector(".login-step1");
const loginStep2 = document.querySelector(".login-step2");
const loginEmailInput = document.getElementById("loginEmail");
const loginNextBtn = document.getElementById("loginNextButton");
const loginOtpInputs = document.querySelectorAll(".login-otp-group input");
const loginVerifyBtn = document.getElementById("loginVerifyButton");
const displayedLoginEmail = document.getElementById("displayedLoginEmail");

let loginOTP = "";

window.addEventListener("load", () => {
    emailjs.init("VBI2S5EbHIb55SZTm");
    loginStep2.style.display = "none";
    loginVerifyBtn.classList.add("disable");
});

const generateLoginOTP = () => Math.floor(1000 + Math.random() * 9000);

loginNextBtn.addEventListener("click", () => {
    const email = loginEmailInput.value;
    loginOTP = generateLoginOTP();

    loginNextBtn.textContent = "⏳ Sending...";
    loginNextBtn.disabled = true;

    const templateParams = {
        OTP: loginOTP,
        email: email
    };

    emailjs.send("service_1q8y3od", "template_xhhpnxr", templateParams)
        .then(() => {
            alert("OTP sent for login verification!");
            loginStep1.style.display = "none";
            loginStep2.style.display = "block";
            displayedLoginEmail.textContent = email;
        })
        .catch(() => {
            alert("Failed to send login OTP.");
        })
        .finally(() => {
            loginNextBtn.textContent = "Send OTP";
            loginNextBtn.disabled = false;
        });
});

loginOtpInputs.forEach((input, idx, arr) => {
    input.addEventListener("keyup", function (e) {
        if (this.value.length >= 1) {
            this.value = this.value[0];
            if (idx < arr.length - 1) arr[idx + 1].focus();
        }

        const allFilled = Array.from(arr).every(i => i.value !== "");
        loginVerifyBtn.classList.toggle("disable", !allFilled);
    });
});

loginVerifyBtn.addEventListener("click", () => {
    const entered = Array.from(loginOtpInputs).map(i => i.value).join("");
    if (entered === loginOTP.toString()) {
        alert("Login OTP matched. Redirecting...");
        document.getElementById("loginOtpForm").submit();
    } else {
        alert("Incorrect OTP. Please try again.");
    }
});
