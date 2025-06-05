const step1 = document.querySelector(".step1");
const step2 = document.querySelector(".step2");
const step3 = document.querySelector(".step3");
const emailAddress = document.getElementById("emailAddress");
const verifyEmail = document.getElementById("verifyEmail");
const inputs = document.querySelectorAll(".otp-group input");
const nextButton = document.getElementById("nextButton");
const verifyButton = document.getElementById("verifyButton");

let OTP = "";

window.addEventListener("load", () => {
    emailjs.init("VBI2S5EbHIb55SZTm");
    step2.style.display = "none";
    step3.style.display = "none";
    nextButton.classList.add("disable");
    verifyButton.classList.add("disable");
});

const validateEmail = (email) => {
    const re = /\S+@\S+\.\S+/;
    if (re.test(email)) {
        nextButton.classList.remove("disable");
    } else {
        nextButton.classList.add("disable");
    }
};

emailAddress.addEventListener("input", () => {
    validateEmail(emailAddress.value);
});

const generateOTP = () => {
    return Math.floor(1000 + Math.random() * 9000);
};

inputs.forEach((input, idx, arr) => {
    input.addEventListener("keyup", function (e) {
        if (this.value.length >= 1) {
            e.target.value = e.target.value.substr(0, 1);
            if (idx < arr.length - 1) {
                arr[idx + 1].focus();
            }
        }

        const allFilled = Array.from(arr).every(input => input.value !== "");
        if (allFilled) {
            verifyButton.classList.remove("disable");
        } else {
            verifyButton.classList.add("disable");
        }
    });
});

nextButton.addEventListener("click", () => {
    const email = emailAddress.value;
    const otp = generateOTP();

    nextButton.innerHTML = "⏳ Sending...";
    nextButton.disabled = true;

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
            alert("OTP SENT!");
            step1.style.display = "none";
            step2.style.display = "block";
            step3.style.display = "none";
            verifyEmail.textContent = email;
        })
        .catch((error) => {
            console.error("FAILED...", error);
            alert("Error while sending OTP. Please try again.");
        })
        .finally(() => {
            nextButton.innerHTML = "Next →";
            nextButton.disabled = false;
        });
});

verifyButton.addEventListener("click", () => {
    const enteredOtp = Array.from(inputs).map(i => i.value).join("");
    const realOtp = sessionStorage.getItem("otp");

    console.log("Entered OTP:", enteredOtp);

    if (enteredOtp === realOtp) {
        alert("OTP match! You can now proceed.");
        step2.style.display = "none";
        step3.style.display = "block";
    } else {
        alert("OTP doesn't match. Try again.");
    }
});
