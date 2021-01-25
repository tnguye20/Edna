import * as React from 'react';
import {
  BrowserRouter as Router,
  Switch
} from 'react-router-dom';


import { ROUTES } from './constants';
import { 
  AuthContextProvider
 } from './contexts';
import { 
  AuthRoute,
  UnAuthRoute,
  Login,
  Signup,
  Signout,
  UploadChat,
  Main
} from './components';

function App() {
  return (
    <AuthContextProvider>
      <Router>
        <Switch>
            <UnAuthRoute path={ ROUTES.LOGIN }>
              <Login />
            </UnAuthRoute>

            <UnAuthRoute path={ ROUTES.SIGNUP }>
              <Signup />
            </UnAuthRoute>

            <AuthRoute path={ ROUTES.SIGNOUT }>
              <Signout />
            </AuthRoute>

            <AuthRoute path={ ROUTES.UPLOAD_CHAT }>
              <UploadChat />
            </AuthRoute>

            <AuthRoute path={ ROUTES.ROOT }>
              <Main />
            </AuthRoute>
        </Switch>
      </Router>
    </AuthContextProvider>
  );
}

export default App;