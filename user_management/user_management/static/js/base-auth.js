document.addEventListener('DOMContentLoaded', function() {
    // Theme Toggle
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const htmlElement = document.documentElement;

    themeToggle.addEventListener('click', function() {
        const currentTheme = htmlElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        htmlElement.setAttribute('data-bs-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        themeIcon.classList.toggle('fa-moon');
        themeIcon.classList.toggle('fa-sun');
    });

    // Set initial theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    htmlElement.setAttribute('data-bs-theme', savedTheme);
    themeIcon.classList.toggle('fa-moon', savedTheme === 'light');
    themeIcon.classList.toggle('fa-sun', savedTheme === 'dark');

    // Password Toggle Visibility
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const passwordInput = this.previousElementSibling;
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            const icon = this.querySelector('i');
            icon.classList.toggle('fa-eye');
            icon.classList.toggle('fa-eye-slash');
        });
    });

    // Password Strength Meter
    const passwordInput = document.getElementById('id_password1');
    const passwordStrengthIndicator = document.getElementById('password-strength');

    if (passwordInput && passwordStrengthIndicator) {
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            const strength = calculatePasswordStrength(password);
            
            passwordStrengthIndicator.textContent = strength.message;
            passwordStrengthIndicator.className = `password-strength ${strength.className}`;
        });
    }

    function calculatePasswordStrength(password) {
        let strength = 0;
        if (password.length >= 8) strength++;
        if (password.match(/[a-z]+/)) strength++;
        if (password.match(/[A-Z]+/)) strength++;
        if (password.match(/[0-9]+/)) strength++;
        if (password.match(/[$@#&!]+/)) strength++;

        switch(strength) {
            case 0:
            case 1:
                return { message: 'Weak Password', className: 'weak' };
            case 2:
            case 3:
                return { message: 'Medium Strength', className: 'medium' };
            default:
                return { message: 'Strong Password', className: 'strong' };
        }
    }

    // Real-time Form Validation
    const registrationForm = document.getElementById('registration-form');
    if (registrationForm) {
        // Email Validation
        const emailInput = document.getElementById('id_email');
        if (emailInput) {
            emailInput.addEventListener('input', function() {
                validateEmail(this);
            });
        }

        // Phone Number Validation
       

        // Password Matching Validation
        const password1Input = document.getElementById('id_password1');
        const password2Input = document.getElementById('id_password2');
        
        if (password1Input && password2Input) {
            password2Input.addEventListener('input', function() {
                validatePasswordMatch(password1Input, password2Input);
            });
        }

        // Form Submission Validation
        registrationForm.addEventListener('submit', function(event) {
            let isValid = true;
            const requiredInputs = this.querySelectorAll('input[required]');

            requiredInputs.forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add('is-invalid');
                    isValid = false;
                } else {
                    input.classList.remove('is-invalid');
                }
            });

            // Additional specific validations
            if (emailInput) {
                isValid = validateEmail(emailInput) && isValid;
            }

            if (phoneInput) {
                isValid = validatePhoneNumber(phoneInput) && isValid;
            }

            if (password1Input && password2Input) {
                isValid = validatePasswordMatch(password1Input, password2Input) && isValid;
            }

            // Terms and Conditions
            const termsCheckbox = document.getElementById('terms');
            if (termsCheckbox && !termsCheckbox.checked) {
                termsCheckbox.classList.add('is-invalid');
                isValid = false;
            }

            if (!isValid) {
                event.preventDefault();
                showFormErrors();
            }
        });
    }

    // Email Validation Function
    function validateEmail(emailInput) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const isValid = emailRegex.test(emailInput.value);
        
        if (!isValid) {
            emailInput.classList.add('is-invalid');
            emailInput.setCustomValidity('Please enter a valid email address');
        } else {
            emailInput.classList.remove('is-invalid');
            emailInput.setCustomValidity('');
        }
        
        return isValid;
    }

    // Phone Number Validation Function (for Rwandan phone numbers)
    function validatePhoneNumber(phoneInput) {
        const phoneRegex = /^(07|78|72|82)\d{7}$/;
        const isValid = phoneRegex.test(phoneInput.value);
        
        if (!isValid && phoneInput.value) {
            phoneInput.classList.add('is-invalid');
            phoneInput.setCustomValidity('Please enter a valid Rwandan phone number');
        } else {
            phoneInput.classList.remove('is-invalid');
            phoneInput.setCustomValidity('');
        }
        
        return isValid;
    }

    // Password Matching Validation
    function validatePasswordMatch(password1Input, password2Input) {
        const isMatching = password1Input.value === password2Input.value;
        
        if (!isMatching) {
            password2Input.classList.add('is-invalid');
            password2Input.setCustomValidity('Passwords do not match');
        } else {
            password2Input.classList.remove('is-invalid');
            password2Input.setCustomValidity('');
        }
        
        return isMatching;
    }

    // Show Form Errors
    function showFormErrors() {
        const firstInvalidInput = document.querySelector('.is-invalid');
        if (firstInvalidInput) {
            firstInvalidInput.focus();
        }
    }

    // Profile Picture Preview
    const profilePictureInput = document.getElementById('id_profile_picture');
    const profilePicturePreview = document.getElementById('profile-picture-preview');

    if (profilePictureInput && profilePicturePreview) {
        profilePictureInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    profilePicturePreview.src = e.target.result;
                    profilePicturePreview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
    }
});




document.addEventListener('DOMContentLoaded', function() {
    // ... (previous theme and password toggle code remains the same)

    // Form Validation
    const registrationForm = document.getElementById('registration-form');
    if (registrationForm) {
        // Email Validation
        const emailInput = document.getElementById('id_email');
        const passwordInput = document.getElementById('id_password');
        const confirmPasswordInput = document.getElementById('id_confirm_password');

        // Email Validation
        if (emailInput) {
            emailInput.addEventListener('input', function() {
                validateEmail(this);
            });
        }

        // Password Validation
        if (passwordInput) {
            passwordInput.addEventListener('input', function() {
                validatePassword(this);
                checkPasswordStrength(this);
            });
        }

        // Confirm Password Validation
        if (confirmPasswordInput) {
            confirmPasswordInput.addEventListener('input', function() {
                validateConfirmPassword(passwordInput, confirmPasswordInput);
            });
        }

        // Form Submission Validation
        registrationForm.addEventListener('submit', function(event) {
            let isValid = true;
            const requiredInputs = this.querySelectorAll('input[required]');

            requiredInputs.forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add('is-invalid');
                    isValid = false;
                } else {
                    input.classList.remove('is-invalid');
                }
            });

            // Specific field validations
            if (emailInput) {
                isValid = validateEmail(emailInput) && isValid;
            }

            if (passwordInput) {
                isValid = validatePassword(passwordInput) && isValid;
                checkPasswordStrength(passwordInput);
            }

            if (confirmPasswordInput) {
                isValid = validateConfirmPassword(passwordInput, confirmPasswordInput) && isValid;
            }

            // Terms and Conditions
            const termsCheckbox = document.getElementById('terms');
            if (termsCheckbox && !termsCheckbox.checked) {
                termsCheckbox.classList.add('is-invalid');
                isValid = false;
            }

            if (!isValid) {
                event.preventDefault();
                showFormErrors();
            }
        });
    }

    // Email Validation Function
    function validateEmail(emailInput) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const isValid = emailRegex.test(emailInput.value);
        
        if (!isValid) {
            emailInput.classList.add('is-invalid');
            emailInput.setCustomValidity('Please enter a valid email address');
        } else {
            emailInput.classList.remove('is-invalid');
            emailInput.setCustomValidity('');
        }
        
        return isValid;
    }

    // Password Validation Function
    function validatePassword(passwordInput) {
        const password = passwordInput.value;
        const isValid = password.length >= 8;
        
        if (!isValid) {
            passwordInput.classList.add('is-invalid');
            passwordInput.setCustomValidity('Password must be at least 8 characters long');
        } else {
            passwordInput.classList.remove('is-invalid');
            passwordInput.setCustomValidity('');
        }
        
        return isValid;
    }

    // Password Strength Checker
    function checkPasswordStrength(passwordInput) {
        const passwordStrengthIndicator = document.getElementById('password-strength');
        const password = passwordInput.value;
        const strength = calculatePasswordStrength(password);
        
        if (passwordStrengthIndicator) {
            passwordStrengthIndicator.textContent = strength.message;
            passwordStrengthIndicator.className = `password-strength ${strength.className}`;
        }
    }

    // Confirm Password Validation
    function validateConfirmPassword(passwordInput, confirmPasswordInput) {
        const isMatching = passwordInput.value === confirmPasswordInput.value;
        
        if (!isMatching) {
            confirmPasswordInput.classList.add('is-invalid');
            confirmPasswordInput.setCustomValidity('Passwords do not match');
        } else {
            confirmPasswordInput.classList.remove('is-invalid');
            confirmPasswordInput.setCustomValidity('');
        }
        
        return isMatching;
    }

    // Password Strength Calculation (from previous implementation)
    function calculatePasswordStrength(password) {
        let strength = 0;
        if (password.length >= 8) strength++;
        if (password.match(/[a-z]+/)) strength++;
        if (password.match(/[A-Z]+/)) strength++;
        if (password.match(/[0-9]+/)) strength++;
        if (password.match(/[$@#&!]+/)) strength++;

        switch(strength) {
            case 0:
            case 1:
                return { message: 'Weak Password', className: 'weak' };
            case 2:
            case 3:
                return { message: 'Medium Strength', className: 'medium' };
            default:
                return { message: 'Strong Password', className: 'strong' };
        }
    }

    // Show Form Errors
    function showFormErrors() {
        const firstInvalidInput = document.querySelector('.is-invalid');
        if (firstInvalidInput) {
            firstInvalidInput.focus();
        }
    }
});