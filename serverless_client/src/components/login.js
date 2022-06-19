import { setCookie, getCookie } from './utils';
import {varifyUserToken} from './index.js';

const userLogin = async (email, password) => {
    try{
        const response = await fetch("https://hwfj65vjz4.execute-api.ap-south-1.amazonaws.com/development/auth/loginUser", {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'auth_id': email,
                'password': password
            })
        });

        const res = await response.json();
        console.log(res);
        if(!response.ok | response.status != 200){
            throw res;
        }

        const access_token = res.access_token;
        console.debug(access_token);
        setCookie('access_token', access_token);

        window.location.replace("./index.html");
    } catch (error){
        console.error('error login', error);
    }
}

if (document.querySelector("#toggleLoginForgetPassword")){
    document.querySelector("#toggleLoginForgetPassword").addEventListener("click", (event) => {
        event.preventDefault();
        document.querySelector("#serverless_auth_forgot_password").classList.toggle("hidden");
        document.querySelector("#serverless_auth_login").classList.toggle("hidden");
    });
}

if (document.querySelector("#serverless_auth_login")) {
    const access_token = getCookie('access_token');
    if (access_token){
        varifyUserToken(access_token);
    }
    document.querySelector("#form-auth-login").addEventListener("submit", event => {
        event.preventDefault();

        const email = document.querySelector("#formloginEmail").value;
        const password = document.querySelector("#formLoginPassword").value;

        if(!email | !password) return;
        userLogin(email, password);
    });
};