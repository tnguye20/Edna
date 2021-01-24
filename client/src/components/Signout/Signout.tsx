import React, { useEffect } from 'react';
import { auth } from '../../libraries';
import { useAuthValue } from '../../contexts';

import {
  Grid,
  Container,
  Typography
} from '@material-ui/core';

export const Signout = () => {
  const { setAuthUser } = useAuthValue();

  useEffect( () => {
    auth.signOut().then( () => {
      setTimeout( () => {
        setAuthUser({
          uid: null,
        });
        localStorage.removeItem("idToken");
        localStorage.removeItem("uid");
      } , 1000 );
    }).catch( err => {
      console.log(err);
    } )
  })

  return (
    <Container maxWidth="md">
      <Grid
        container
        spacing={0}
        direction="column"
        justify="center"
        style={{ minHeight: '100vh'}}
      >
        <Grid item xs={12} sm={12}>
          <Typography
            align="center"
            variant="h1"
            component="h2"
            gutterBottom
          >
            Signing Out...
          </Typography>
        </Grid>
      </Grid>
    </Container>
  )
}
