import { getCookie } from './utils';

const varifyUserToken = async (access_token) => {
    try{
        const response = await fetch(`https://hwfj65vjz4.execute-api.ap-south-1.amazonaws.com/development/auth/getUserAccess/${access_token}`, {
            method: 'GET'
        });

        const res = await response.json();
        console.log(res);
        if(!response.ok | response.status != 200){
            throw res;
        }

        const user = res.user;
        console.debug(user);

        window.location.replace("./index.html");
    } catch (error){
        console.error('error login', error);
        // window.location.replace("./login.html");
    }
}

if (window.location.pathname === '/index.html'){
    const access_token = getCookie('access_token');
    console.log(access_token)
    if(!access_token){
        window.location.replace('./login.html');
    }else{
        varifyUserToken(access_token);
    }

}

export {varifyUserToken};