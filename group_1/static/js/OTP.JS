const step1 = document.querySelector(".step1");
const step2 = document.querySelector(".step2");
const step3 = document.querySelector(".step3");

const emailAddress = document.getElementById("emailAddress");
const nextButton = document.getElementById("nextButton");
const verifyButton = document.getElementById("verifyButton");
const verifyEmail = document.getElementById("verifyEmail");
const inputs = document.querySelectorAll(".otp-group input");

let OTP = "";


window.addEventListener("load", () => {
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
 
    const username = document.getElementById("username").value;
    const email = emailAddress.value;
    const password = document.getElementById("password").value;

    if (!username || !email || !password) {
        alert("Lengkapi semua field terlebih dahulu.");
        return;
    }

    sessionStorage.setItem("username", username);
    sessionStorage.setItem("email", email);
    sessionStorage.setItem("password", password);

    sendOTP();
});


function sendOTP() {
    const email = sessionStorage.getItem("email");
    OTP = generateOTP();

    nextButton.innerHTML = "⏳ Sending...";
    nextButton.disabled = true;

    sessionStorage.setItem("otp", OTP);

    const templateParams = {
        OTP: OTP,
        email: email
    };

    const serviceID = 'service_1q8y3od';     
    const templateID = 'template_xhhpnxr';  

    emailjs.send(serviceID, templateID, templateParams)
        .then(() => {
            alert("OTP sent to " + email);
            step1.style.display = "none";
            step2.style.display = "block";
            verifyEmail.textContent = email;
        })
        .catch((error) => {
            console.error("OTP failed to send:", error);
            alert("Error sending OTP. Please try again.");
        })
        .finally(() => {
            nextButton.innerHTML = "Next →";
            nextButton.disabled = false;
        });
}


verifyButton.addEventListener("click", () => {
    const enteredOtp = Array.from(inputs).map(i => i.value).join("");
    const realOtp = sessionStorage.getItem("otp");

    if (enteredOtp === realOtp) {
        alert("OTP Verified!");

        step2.style.display = "none";
        step3.style.display = "block";

        const username = document.getElementById("username").value;
        const email = document.getElementById("emailAddress").value;
        const password = document.getElementById("password").value;

        fetch("/register_user", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, email, password })
        })
        .then(res => res.json())
        .then(data => {
            alert(data.message || "Registration successful!");

            window.location.href = "/login";
        })
        .catch(err => {
            console.error(err);
            alert("Registration failed.");
        });
    } else {
        alert("OTP does not match. Please try again.");
    }
});


function resendOTP() {
    sendOTP();
}
