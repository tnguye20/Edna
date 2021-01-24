import React, { FunctionComponent} from 'react';
import { useAuthValue } from '../../contexts';
import { Route, Redirect } from 'react-router-dom';
import { ROUTES } from '../../constants/';

export const AuthRoute: FunctionComponent<any> = ({children, ...rest}) => {
  const { authUser } = useAuthValue();

  return (
    <Route
      {...rest}
      render={
        ({ location }) => (
          authUser.uid !== null ? (
            children
          ) : (
            <Redirect
              to={{
                pathname: ROUTES.LOGIN,
                state: { from: location }
              }}
            />
          )
        )
      }
    />
  )
}

export const UnAuthRoute: FunctionComponent<any> = ({children, ...rest}) => {
  const { authUser } = useAuthValue();

  return (
    <Route
      {...rest}
      render={
        ({ location }) => (
          authUser.uid === null ? (
            children
          ) : (
            <Redirect
              to={{
                pathname: ROUTES.ROOT,
                state: { from: location }
              }}
            />
          )
        )
      }
    />
  )
}

export const StaticRoute: FunctionComponent<any> = ({children, ...rest}) => {
  return (
    <Route
      {...rest}
      render={ () => (
        children
      )}
    />
  )
}