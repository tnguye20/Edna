import React from 'react';
import {
  Grid,
  Container,
  Typography
} from '@material-ui/core';
import { Link } from 'react-router-dom';
import { LoginForm } from '../LoginForm';

export const Login = () => {
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
          <Link to="/" className="header">
            <Typography
              align="center"
              variant="h2"
              component="h3"
              gutterBottom
            >
              The Edna
            </Typography>
          </Link>
          <LoginForm />
        </Grid>
      </Grid>
    </Container>
  )
}
