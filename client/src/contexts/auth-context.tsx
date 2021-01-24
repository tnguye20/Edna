import * as React from 'react';
import { useAuth } from '../hooks';

const { createContext, useContext } = React;

export const AuthContext = createContext<Partial<any>>({});
 
export const AuthContextProvider: React.FunctionComponent = (props) => {
    const { children } = props;
    const { authUser, setAuthUser } = useAuth();

    return (
        <AuthContext.Provider value={{
            authUser,
            setAuthUser
        }}>
            { children }
        </AuthContext.Provider>
    )
}

export const useAuthValue = () => useContext(AuthContext);