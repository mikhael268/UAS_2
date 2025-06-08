import emailjs from 'https://cdn.emailjs.com/dist/email.min.mjs';

document.addEventListener("DOMContentLoaded", function () {
    // Inisialisasi EmailJS
    emailjs.init("VBI2S5EbHIb55SZTm"); // Ganti dengan public key dari EmailJS

    const otpForm = document.getElementById("otpForm");
    const otpInput = document.getElementById("otpInput");

    // Jika di halaman register_otp.html
    if (otpForm && otpInput) {
        otpForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const userOtp = otpInput.value;
            const realOtp = localStorage.getItem("otp");
            const userData = JSON.parse(localStorage.getItem("temp_user"));

            if (!userData || !realOtp) {
                alert("Session expired. Please register again.");
                window.location.href = "/signup";
                return;
            }

            if (userOtp === realOtp) {
                // Kirim data ke backend
                fetch("/complete-registration", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ email: userData.email }),
                })
                    .then((res) => {
                        if (res.ok) {
                            alert("Registration successful!");
                            localStorage.removeItem("otp");
                            localStorage.removeItem("temp_user");
                            window.location.href = "/login";
                        } else {
                            alert("Failed to complete registration.");
                        }
                    })
                    .catch((err) => {
                        console.error("Error:", err);
                        alert("Server error.");
                    });
            } else {
                alert("Invalid OTP. Please try again.");
            }
        });
    }

    // Jika di halaman signUp.html
    const signupForm = document.getElementById("signupForm");
    if (signupForm) {
        signupForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const username = document.getElementById("username").value;
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            // Generate OTP dan simpan di localStorage
            const otp = Math.floor(100000 + Math.random() * 900000);
            localStorage.setItem("otp", otp.toString());
            localStorage.setItem("temp_user", JSON.stringify({ username, email, password }));

            // Kirim OTP via EmailJS
            emailjs.send("service_1q8y3od", "template_xhhpnxr", {
                to_email: email,
                otp: otp,
            }).then(() => {
                // Lanjut ke halaman verifikasi OTP
                window.location.href = `/signup`; // biar backend redirect ke register_otp.html
            }).catch((error) => {
                console.error("EmailJS error:", error);
                alert("Failed to send OTP. Please try again.");
            });
        });
    }
});
