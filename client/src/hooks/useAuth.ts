import * as React from 'react';
import { auth } from '../libraries';

const { useState, useEffect } = React;

export const useAuth = () => {
    const idToken = localStorage.getItem('idToken');
    const uid = localStorage.getItem('uid');
    const [authUser , setAuthUser] = useState(
        { uid, idToken }
    );

    useEffect(() => {
        const unsubscribe = auth.onAuthStateChanged( (user) => {
          if(user){
            user.getIdToken(true).then( (idToken) => {
              localStorage.setItem("idToken", idToken);
              localStorage.setItem("uid", user.uid);
              setAuthUser({
                ...user,
                idToken
              });
            })
          }
        });
    
        return () => unsubscribe()
    }, []);

    return {
        authUser,
        setAuthUser
    }
}