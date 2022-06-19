function validateInputData(name, email, password){
    if(!name | name.length < 3){
        console.error("Invalid name");
        return false
    }
    if(!email | email.length < 7){
        console.error("Invalid Email");
        return false;
    }
    if(!password | password.length < 8){
        console.error("Invalid Password");
    }
    return true;

}

const confirmUserSignup = async (user_id, email, confirm_code) => {
    try{
        const response = await fetch("https://hwfj65vjz4.execute-api.ap-south-1.amazonaws.com/development/auth/confirmSignup", {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'user_id': user_id,
                'email': email,
                'confirmation_code': confirm_code,
            })
        });

        const res = await response.json();
        console.log(res);
        if(!response.ok | response.status != 200){
            throw res;
        }

        window.location.replace("./login.html");
    } catch (error){
        console.error('error Confirm singup:', error);
        if (error.code === "INTERNAL_SERVER_ERROR") {
            alert(error.message);
        }
    }
}

const userSignUp = async (name, email, password) => {
    try{
        const response = await fetch("https://hwfj65vjz4.execute-api.ap-south-1.amazonaws.com/development/auth/signupUser", {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'name': name,
                'email': email,
                'password': password,
            })
        });

        const res = await response.json();
        console.log(res);
        if(!response.ok | response.status != 200){
            throw res;
        }

        const user_id = res.UserSub;
        console.debug(user_id);

        document.querySelector("#serverless_auth_singup").classList.add('hidden');
        document.querySelector("#serverless_auth_confirm_signup").classList.remove('hidden');
        document.querySelector("#formConfirmEmail").value = email;
        document.querySelector("#formConfirmEmail").setAttribute('data-user-id', user_id);
    } catch (error){
        console.error('error signing up:', error);
        // if (error.code === "INTERNAL_SERVER_ERROR") {
        //     alert(error.message);
        //     window.location.replace("./signup.html");
        // }
    }
}

if (document.querySelector("#serverless_auth_singup")) {
    document.querySelector("#form-auth-signup").addEventListener("submit", event => {
        event.preventDefault();

        const name = document.querySelector("#formSignUpName").value;
        const email = document.querySelector("#formSignUpEmail").value;
        const password = document.querySelector("#formSignUpPassword").value;

        if(!validateInputData(name, email, password)) return;
        userSignUp(name, email, password);
    });
};

if (document.querySelector('#serverless_auth_confirm_signup')) {
    if (!document.querySelector("#formConfirmEmail").getAttribute('data-user-id')){
        document.querySelector("#serverless_auth_singup").classList.remove('hidden');
        document.querySelector("#serverless_auth_confirm_signup").classList.add('hidden');
    }
    document.querySelector("#form-auth-confirm-signup").addEventListener("submit", event => {
        event.preventDefault();

        const email = document.querySelector("#formConfirmEmail");
        const confirm_code = document.querySelector("#formConfirmCode")
        const user_id = email.getAttribute('data-user-id');
        if(!email && !confirm_code){
            console.error('Invalid email and code.')
        }
        confirmUserSignup(user_id, email.value, confirm_code.value);
    });
}
